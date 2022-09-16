import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
from scipy.fft import fft, ifft, ifftshift, fftshift
import sys

#read in the data from the log file
log_file = 'G:\SAXS-WAXS-Data-Analysis\Cu_foil_fdbkOff_8950_9450_5_1s_3f_160922_2100_run3\images\livelogfile.log'
file = open(log_file, 'r')
lines = file.read().splitlines()
file.close()
n_rows = np.shape(lines)[0]
print(n_rows)
I0 = np.zeros(n_rows)
Energy = np.zeros(n_rows)
for i in range(n_rows):
    splitline = lines[i].split(" ")
    #print(splitline.index('Ibs'))
    I0_temp = splitline[17].split('"')
    I0_temp = int(I0_temp[1])
    I0[i]=I0_temp
    Energy_temp = splitline[87].split('"')
    Energy_temp = float(Energy_temp[1])
    Energy[i]=Energy_temp
#sys.exit()

#directory which contains all the folders which contain the data (Spool.dat) files
master_dir = 'G:\SAXS-WAXS-Data-Analysis\Cu_foil_fdbkOff_8950_9450_5_1s_3f_160922_2100_run3\spool'
#we need to first determine how many spool data files we actually have
n_spool=0
#loop through all directories and if we find a file that starts with Spool (case sensitive) we add it to the list
for path, currentDirectory, files in os.walk(master_dir):
    for file in files:
        if file.startswith("Spool"):
            #define the total number of spool files we have
            n_spool+=1

print(n_spool)
#dimensions of the pixel detector
dim = 2048
#number of scans for spool data file
scanperdat = 3
#total number of meaured energies we have
n_points = n_spool*scanperdat
#create an array to hold all the absorption values, -1 as first enrty is blank
attenuation=np.zeros(n_points)
raw_absorption =np.zeros(n_points)
#get list of all folders containing data
Dir_list = os.listdir(master_dir)
#filter out ony folders that dont begin with spool so we know how many folders
#   we are working with
filtered_list=[word for word in Dir_list if word.startswith('Spool')]

i=0
#looping over each spool folder
for index1 in range(np.shape(filtered_list)[0]):
    #get the names of all spool foiles iside the folder
    New_Spool_Dir = os.listdir(master_dir+'\SpoolDirectory'+str(index1))
    print(index1)
    #looping over each of these files
    for (index2, name2) in enumerate(New_Spool_Dir):
        file = master_dir+'\SpoolDirectory'+str(index1)+'/'+name2
        #read in the data from the file
        data = np.fromfile(file, dtype=np.int16)
        for index3 in range(scanperdat):
            #we know that for the test data the first entry has nothing in it so
            #   it will be taken as the blank but this may need to be updated for future data sets
            if index1 == 0 and index2 == 0 and index3 == 0:
                blank = data[index3*dim**2:(index3+1)*dim**2].reshape(dim,dim)
                data_array = data[index3*dim**2:(index3+1)*dim**2].reshape(dim,dim)-blank
                slice = np.sum(data_array,1)
                recon = ifftshift(ifft(slice))
                absorption = np.sqrt(abs(max(recon))*abs(max(recon)))
                attenuation[i] = 0#1.0*I0[i]/absorption
                raw_absorption[i] = 0# absorption
                #attenuation[i] = absorption
                phase = np.unwrap(np.angle(recon))
            else:
                data_array = data[index3*dim**2:(index3+1)*dim**2].reshape(dim,dim)-blank
                #sum all the data accross the horizonal axis so we are jsut left
                #   with the integrated intensity allong the vertical direction of the detector
                maximum=np.where(data_array == np.amax(data_array))
                #print(maximum)
                slice = np.sum(data_array[maximum[0][0]-150:maximum[0][0]+150,maximum[1][0]-500:maximum[1][0]+500])#data_array[:,1024]#
                #hot fix for this one annomalous data point
                #slice[1026]=(1.0*slice[1025]+slice[1027])/2.0
                #reconstruct the Transmission function by taking the inverse fourier transform
                #recon = ifftshift(ifft(slice))
                #the absorption is just the magnitude of the maximum value of the Transmission function
                absorption = slice#np.sqrt(abs(max(recon))*abs(max(recon)))
                attenuation[i] = 1.0*I0[i]/absorption
                raw_absorption[i] = absorption
                #print(I0[i])
                #extract the phase by effectivelly wrapping it between -pi and pi
                #phase = np.unwrap(np.angle(recon))
                #we usually have more spool files than actual data points so if we
                #   go over the limit just exit the loop
                if i >= n_rows-1:
                    break
            i+=1
#we now need to average over every 3 points as they are repeated measurements
new_attenuation=np.zeros(n_spool)
new_energy=np.zeros(n_spool)
new_raw = np.zeros(n_spool)
new_I0 = np.zeros(n_spool)
j=0
for i in range(n_spool):
    new_attenuation[i]=np.mean(attenuation[i*scanperdat:(i+1)*scanperdat])
    new_energy[i]=np.mean(Energy[i*scanperdat:(i+1)*scanperdat])
    new_raw[i]=np.mean(raw_absorption[i*scanperdat:(i+1)*scanperdat])
    new_I0[i] = np.mean(I0[i*scanperdat:(i+1)*scanperdat])
#neglect the first point as the first measurement is usually blank
attenuation = new_attenuation[1:n_spool]
Energy = new_energy[1:n_spool]
raw_absorption = new_raw[1:n_spool]
I0 = new_I0[1:n_spool]

#plot the results as both line and scatter plots
fig, axs = plt.subplots(2)
axs[0].plot(Energy,attenuation)
axs[1].scatter(Energy,attenuation,s=1)
plt.xlabel("Energy (keV)")
plt.ylabel("I0/Absorption")

fig, axs = plt.subplots(2)
axs[0].plot(Energy,I0)
axs[1].scatter(Energy,I0,s=1)
plt.xlabel("Energy (keV)")
plt.ylabel("I0")

fig, axs = plt.subplots(2)
axs[0].plot(Energy,raw_absorption)
axs[1].scatter(Energy,raw_absorption,s=1)
plt.xlabel("Energy (keV)")
plt.ylabel("Absorption")
plt.show()