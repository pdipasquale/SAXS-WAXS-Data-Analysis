import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
from scipy.fft import fft, ifft, ifftshift, fftshift
import sys

#read in the data from the log file
log_file = 'F:/SAXS-WAXS-Data-Analysis/Cu_Sample1_8929_9479_6s_8f_200922_1925_att3/images/livelogfile.log'
#log_file = 'G:/SAXS-WAXS-Data-Analysis/Ni_Sample1_8282_8832_2p5s_8f_210922_0427_att0_run2/images/livelogfile.log'

#sys.exit()

#directory which contains all the folders which contain the data (Spool.dat) files
master_dir = 'F:/SAXS-WAXS-Data-Analysis/Cu_Sample1_8929_9479_6s_8f_200922_1925_att3/spool'
#master_dir = 'G:/SAXS-WAXS-Data-Analysis/Ni_Sample1_8282_8832_2p5s_8f_210922_0427_att0_run2/spool'
#we need to first determine how many spool data files we actually have

n_itts = 10 #What does this variable represent?

file = open(log_file, 'r')
lines = file.read().splitlines()
file.close()
n_rows = np.shape(lines)[0]
print('Logfile rows: ', n_rows)
I0 = np.zeros(n_rows)
Energy = np.zeros(n_rows)
dark = []
for i in range(n_rows):
    splitline = lines[i].split(" ")
    name = splitline[splitline.index('chanh_filename')+2].split('"')[1]
    split_name=name.split('_')
    if ('dark' in split_name):
        dark.append(i)

    I0_temp = splitline[17].split('"')
    I0_temp = int(I0_temp[1])
    I0[i]=I0_temp
    Energy_temp = splitline[87].split('"')
    Energy_temp = float(Energy_temp[1])
    Energy[i]=Energy_temp
print((dark))
n_rows-=np.shape(dark)[0]

#Get the dark current logfile measurements to subtract from I0 later.
dark_logfile = np.zeros(np.shape(dark)[0])
dark_index = 0
for i in dark:
    dark_logfile[dark_index] = int(lines[i].split(" ")[17].split('"')[1])
    print(int(lines[i].split(" ")[17].split('"')[1]))
    dark_index+=1
dark_ave = np.mean(dark_logfile)

I0=np.delete(I0, dark)
Energy=np.delete(Energy, dark)
print('Dark current measurements removed from the I0 and energy arrays')
#sys.exit()
n_spool=0
#loop through all directories and if we find a file that starts with Spool (case sensitive) we add it to the list
for path, currentDirectory, files in os.walk(master_dir):
    for file in files:
        if file.startswith("Spool"):
            #define the total number of spool files we have
            n_spool+=1


#dimensions of the pixel detector
dim = 2048
#number of scans for spool data file
scanperdat = 3

scans_per_e = 8

print(n_spool, (n_spool+4)*scanperdat,n_spool*scanperdat/scans_per_e)
#total number of meaured energies we have
n_points = n_spool*scanperdat
#create an array to hold all the absorption values, -1 as first enrty is blank
attenuation=np.zeros(int(n_rows/scans_per_e))
print(n_rows,n_rows/scans_per_e)
raw_absorption =np.zeros(int(n_rows/scans_per_e))
phase_all = np.zeros((int(n_rows/scans_per_e)))
phase_ave = np.zeros(((int(n_rows/scans_per_e)),n_itts))
phase_energy_surface=np.zeros((int(n_rows/scans_per_e),dim))
#get list of all folders containing data
Dir_list = os.listdir(master_dir)
#filter out ony folders that dont begin with spool so we know how many folders
#   we are working with
filtered_list=[word for word in Dir_list if word.startswith('Spool')]

i=0
#go through and find all the files with blank data and average them together
blank=np.zeros((dim,dim))
for index in dark:
    dark_i_1 = int(index/3)
    dark_i_2 = index%3
    dark_i_11 = int(dark_i_1/10)
    dark_file= master_dir+'/SpoolDirectory'+str(dark_i_11)+'/'+'SpoolData'+str(dark_i_1)+'.dat'
    blank += (np.fromfile(dark_file, dtype=np.int16))[dark_i_2*dim**2:(dark_i_2+1)*dim**2].reshape(dim,dim)#/np.shape(dark)[0]

blank = blank/np.shape(dark)[0] #Take average of the blanks.

slice = np.zeros(dim)

#sys.exit()
k=0
#looping over each spool folder
for index1 in range(np.shape(filtered_list)[0]):
    #get the names of all spool foiles iside the folder
    New_Spool_Dir = os.listdir(master_dir+'\SpoolDirectory'+str(index1))

    #looping over each of these files
    for (index2, name2) in enumerate(New_Spool_Dir):
        file = master_dir+'\SpoolDirectory'+str(index1)+'/'+name2
        #read in the data from the file
        data = np.fromfile(file, dtype=np.int16)
        print(index1,index2)
        for index3 in range(scanperdat):
            #print((index1*10+index2)*3+index3)
            if (index1*10+index2)*3+index3 in dark:
                print('skip')
                continue



            data_array = data[index3*dim**2:(index3+1)*dim**2].reshape(dim,dim)-blank
            #sum all the data accross the horizonal axis so we are jsut left
                #with the integrated intensity allong the vertical direction of the detector
            maximum=np.where(data_array == np.amax(data_array))
            #Plot a horizontal/vertical line that intersects the maximum index.
            # graph = plt.plot(data_array[:,maximum[1][0]])
            # grapha = plt.plot(data_array[:,maximum[0][0]])
            # graph2 = plt.plot(data_array[maximum[1][0],:])
            # plt.show()

            if i ==640:
                fig, axs = plt.subplots(2,sharex=True,gridspec_kw={'hspace': 0})
                print('The case i=640 has been found')

                roi = 100
                slice_surface=np.zeros((2048,roi))
                recon_surface= np.zeros((2048,roi))
                phase_surface= np.zeros((2048,roi))
                for ii in range(roi):
                    slice_2 = data_array[:,maximum[1][0]-int(roi/2)+ii]
                    recon_2 = ifftshift(ifft(slice_2))
                    #recon_2 = ifftshift(ifft(slice_2/(I0[i]-dark_ave)))
                    center = np.where(np.abs(recon_2) == np.amax(np.abs(recon_2)))[0][0]
                    phase_2 = np.unwrap(np.angle(recon_2))
                    phase_2 -=phase_2[center]
                    recon_surface[:,ii]=np.abs(recon_2)
                    phase_surface[:,ii]=phase_2
                    slice_surface[:,ii]=slice_2
                    #axs[0].plot(np.abs(recon_2))
                    #axs[0].set_ylabel("Reconstruction")
                    #axs[1].plot(phase_2)
                    #axs[1].set_ylabel("Phase")
                    #plt.xlabel("Pixels")
                x = np.linspace(0,2048-1,2048)
                y = np.linspace(0,roi-1,roi)
                x_2d, y_2d =np.meshgrid(y,x)
                print(np.shape(x_2d))
                print(np.shape(y_2d))
                fig = plt.figure(figsize=(6,5))
                ax = fig.add_subplot(111)#, projection='3d')
                ax.pcolormesh(x_2d, y_2d, slice_surface,cmap='rainbow')
                fig = plt.figure(figsize=(6,5))
                ax = fig.add_subplot(111)#, projection='3d')
                ax.pcolormesh(x_2d, y_2d, recon_surface,cmap='rainbow')
                #ax.plot_wireframe(x_2d, y_2d, recon_surface,color='black')
                fig = plt.figure(figsize=(6,5))
                ax = fig.add_subplot(111)#, projection='3d')
                ax.pcolormesh(x_2d, y_2d, phase_surface,cmap='rainbow')
                #ax.plot_wireframe(x_2d, y_2d, phase_surface,color='black')

            slice += data_array[:,1024]/(I0[i]-dark_ave)#np.sum(data_array[:,maximum[1][0]-200:maximum[1][0]+200],1)#np.sum(data_array,1)#

            if (i+1)%scans_per_e == 0:
                recon = ifftshift(ifft(slice))

                #reconstruct the Transmission function by taking the inverse fourier transform
                #recon = ifftshift(ifft(slice))#ifftshift(ifft(ifftshift(slice)))#

                #the absorption is just the magnitude of the maximum value of the Transmission function
                absorption = np.sqrt(abs(max(recon))*abs(max(recon)))#np.sum(slice)#slice#  #Ask Daniel about this line.
                attenuation[int(i/scans_per_e)] = 1.0/absorption #Removed (I0[i]-dark_ave) from numerator.
                raw_absorption[int(i/scans_per_e)] = absorption

                center = 1024#np.where(np.abs(recon) == np.amax(np.abs(recon)))[0][0]
                #print(I0[i])
                #extract the phase by effectivelly wrapping it between -pi and pi
                phase = np.unwrap(np.angle(recon))
                phase-=phase[center]
                phase_all[int(i/scans_per_e)]=phase[1036]*(-1)
                phase_energy_surface[int(i/scans_per_e),:]=phase
                j=0
                for offset in np.linspace(0,99,n_itts,dtype='int'):
                    #print(int(round(offset/n_itts)))
                    #offset = j
                    #preferably odd
                    center = 1024
                    width = 1
                    range_x = np.linspace(center+offset-int(width/2),center+offset+int(width/2),width,dtype='int')

                    rec_iso = recon[range_x]
                    phase_ave[int(i/scans_per_e),j] = np.mean(phase[range_x])*(-1)
                    j+=1

                if i ==399:
                    fig, axs = plt.subplots(3,sharex=True,gridspec_kw={'hspace': 0})
                    fig.suptitle('SpoolData'+str(index1*10+index2)+', Scan '+str(index3+1)+', Energy='+str(round(Energy[i],3))+'keV')
                    axs[0].plot(slice)
                    axs[0].set_ylabel("Insensity")
                    axs[1].plot(np.abs(recon))
                    axs[1].set_ylabel("Reconstruction")
                    axs[2].scatter(np.linspace(0,dim-1,dim,dtype='int'),phase,s=1)
                    axs[2].set_ylabel("Phase")
                    plt.xlabel("Pixels")
                slice = np.zeros(dim)



            #NORMALISE BY I0!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            #we usually have more spool files than actual data points so if we
                #go over the limit just exit the loop
            #center = np.where(np.abs(recon) == np.amax(np.abs(recon)))[0][0]





            if i >= n_rows-1:
                break
            i+=1

#we now need to average over every 3 points as they are repeated measurements
#new_attenuation=np.zeros(n_spool)
new_energy=np.zeros(int(n_spool*scanperdat/scans_per_e))
#new_raw = np.zeros(n_spool)
new_I0 = np.zeros(int(n_spool*scanperdat/scans_per_e))
#new_phase_ave = np.zeros((n_spool,n_itts))
#new_phase_energy_surface=np.zeros((n_spool,dim))
j=0

for i in range(int(n_spool*scanperdat/scans_per_e)):
#    new_attenuation[i]=np.mean(attenuation[i*scans_per_e+1:(i+1)*scans_per_e+1])
    new_energy[i]=np.mean(Energy[i*scans_per_e+1:(i+1)*scans_per_e+1])
#    new_raw[i]=np.mean(raw_absorption[i*scans_per_e+1:(i+1)*scans_per_e+1])
    new_I0[i] = np.mean(I0[i*scans_per_e+1:(i+1)*scans_per_e+1])
#    for j in range(n_itts):
#        new_phase_ave[i,j] = np.mean(phase_ave[i*scans_per_e+1:(i+1)*scans_per_e+1,j])
#    for j in range(dim):
#        new_phase_energy_surface[i,j] = np.mean(phase_energy_surface[i*scans_per_e+1:(i+1)*scans_per_e+1,j])
#neglect the first or last point as the they are usually blank
#attenuation = new_attenuation[0:n_spool-2]#[1:n_spool]
Energy = new_energy#[0:n_spool-2]#[1:n_spool]
#raw_absorption = new_raw[0:n_spool-2]#[1:n_spool]
I0 = new_I0#[0:n_spool-2]#[1:n_spool]
#phase_ave = new_phase_ave[0:n_spool-2,:]#[1:n_spool]
#phase_energy_surface = new_phase_energy_surface[0:n_spool-2,:]

print(np.where(raw_absorption < 0.00001))
#upper = min(np.where(raw_absorption < 0.00001)[0],np.shape(Energy)[0])
#x = np.linspace(0,2048-1,2048)
#y = Energy
#x_2d, y_2d =np.meshgrid(x,y)
#print(np.shape(x_2d))
#print(np.shape(y_2d))
#fig = plt.figure(figsize=(6,5))
#ax = fig.add_subplot(111)#, projection='3d')
#ax.pcolormesh(x_2d, y_2d, phase_energy_surface,cmap='rainbow')

#plot the results as both line and scatter plots
fig, axs = plt.subplots(2,sharex=True,gridspec_kw={'hspace': 0})
axs[0].plot(Energy[0:int(n_rows/scans_per_e)],attenuation)
axs[1].scatter(Energy[0:int(n_rows/scans_per_e)],attenuation,s=1)
plt.xlabel("Energy (keV)")
plt.ylabel("I0/Absorption")

fig, axs = plt.subplots(2,sharex=True,gridspec_kw={'hspace': 0})
axs[0].plot(Energy,I0)
axs[1].scatter(Energy,I0,s=1)
plt.xlabel("Energy (keV)")
plt.ylabel("I0")

fig, axs = plt.subplots(2,sharex=True,gridspec_kw={'hspace': 0})
axs[0].plot(Energy[0:int(n_rows/scans_per_e)],raw_absorption)
axs[1].scatter(Energy[0:int(n_rows/scans_per_e)],raw_absorption,s=1)
plt.xlabel("Energy (keV)")
plt.ylabel("Absorption")

fig, axs = plt.subplots(2,sharex=True,gridspec_kw={'hspace': 0})
axs[0].plot(Energy[0:int(n_rows/scans_per_e)][0:int(n_rows/scans_per_e)],phase_all)
axs[1].scatter(Energy[0:int(n_rows/scans_per_e)],phase_all,s=1)
plt.xlabel("Energy (keV)")
plt.ylabel("Phase")

i=0

rang= np.linspace(0,99,n_itts,dtype='int')
#rang = np.linspace(0,99,n_itts,dtype='int')
fig, axs = plt.subplots(5,2)#,gridspec_kw={'hspace': 0})
flag1 = 0
flag2 = 0
for i in range(n_itts):
    if i >4 and flag2 != 1:
        flag2 = 1
        flag1=0
    axs[flag1,flag2].set_title('Offset='+str(rang[i]))
    axs[flag1,flag2].plot(Energy[0:int(n_rows/scans_per_e)],phase_ave[:,i])#-phase_ave[:,0])
    #axs[1].scatter(Energy,phase_ave,s=1)
    plt.xlabel("Energy (keV)")
    plt.ylabel("Phase")
    flag1+=1
plt.show()
