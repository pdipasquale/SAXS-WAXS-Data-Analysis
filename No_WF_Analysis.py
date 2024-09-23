import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dat_to_tif import dat_to_tif
from PIL import Image
import os
from scipy.fft import ifft, ifftshift, fftshift
from transmission import *
import datetime
import json
from alive_progress import alive_bar

run_name = "NiFF_MainSection1" #Scan name goes here
spool_name = "NiFF_MainSection1"

master_path = "Z:/Cycle_2024_1/Tran_21019/"
master_spools = "Y:/"
path_to_tifs = master_path + "converted_tifs/" + run_name + "/"
path_to_spools = master_spools + spool_name + "/spool_1/"

path_to_log = path_to_tifs
path_to_json = master_path + run_name + "/scatterbrain/livelogfile.json"

class Logfile:
    def __init__(self, fpath, fname_key = "chanh_filename"):
        self.data = pd.read_json(fpath, lines=True)
        self.fname_key = fname_key

    # You shouldn't use this ... but I know you will 
    # GO FUCK YOURSELF THIS IS CANCER YOU WILL UNDERSTAND TOMORROW
    # I WILL TAKE YOU TO YOUR FUCKING 2D PLANE AND KILL YOU IN 3 DIMENSIONS
    def dark_indices(self):
        df = self.data
        return df.loc[df['chanh_filename'].str.contains('dark')].index

    # Gives entries in the dataframe which contain dark field:
    def get_df(self):
        df = self.data
        return df.loc[df['chanh_filename'].str.contains('dark')]
    
    def get_wf(self):
        df = self.data
        return df.loc[df['chanh_filename'].str.contains('thru')]
    
    def get_sample(self):
        df = self.data
        return df.loc[~(df['chanh_filename'].str.contains('thru') | df['chanh_filename'].str.contains('dark'))]

    def no_df(self, key=None):
        df = self.data
        if key is None:
            return df.loc[~df['chanh_filename'].str.contains('dark')]
        
        return df.loc[~df['chanh_filename'].str.contains('dark'), key]
    
    def no_wf(self):
        df = self.data
        return df.loc[~df['chanh_filename'].str.contains('thru')]

    def no_dfwf(self):
        df = self.data
        return df.loc[
            ~(df['chanh_filename'].str.contains('dark') 
            | df['chanh_filename'].str.contains('thru'))]

    def white_indices(self):
        wf = self.data
        return wf.loc[wf['chanh_filename'].str.contains('thru')].index
    
    def no_wf(self, key=None):
        wf = self.data
        if key is None:
            return wf.loc[~wf['chanh_filename'].str.contains('thru')]
        
        return wf.loc[~wf['chanh_filename'].str.contains('thru'), key]
    
    def just_wf(self, key=None):
        wf = self.data
        if key is None:
            return wf.loc[wf['chanh_filename'].str.contains('thru')]
        
        return wf.loc[wf['chanh_filename'].str.contains('thru'), key]

print(f'path to tifs = {path_to_tifs}')
print(f'path to json = {path_to_json}')

spool_log_name = "spool_num.txt"

scan_log = Logfile(path_to_json)

#print(scan_log.data['chanh_filename'])

# Create the folder to store tifs if it doens't exist
try: 
    os.mkdir(path_to_tifs)
except:
    print("Directory exists, reading...")

# Create the spool log if it doesn't exist, otherwise read 
# the current spool
if spool_log_name not in os.listdir(path_to_log):
    with open(path_to_log + spool_log_name, 'w') as spool_log:
        print("spool_num.txt not found, starting a new log at 0")
        cur_spool = 0
        spool_log.write(str(cur_spool))
else:
    with open(path_to_log + spool_log_name, 'r') as spool_log:
            
        cur_spool = int(spool_log.readline().strip())
        print("spool_num.txt found, reading the last spool number:" + str(cur_spool))

# Map out the directory containing spools and order them

spool_dir_name = 'SpoolDirectory'
dir_entries = [i for i in os.listdir(path_to_spools) if spool_dir_name in i]
spools_seq = sorted(dir_entries, key = lambda n : int(n[len(spool_log_name)+1:]))

count = (3*cur_spool)
for (index, spool_file) in enumerate(spools_seq[cur_spool:], 1):
    for dat in os.listdir(path_to_spools+spool_file):
        print(f'Processing from file {spool_file}:\n\t {dat}')
        dat_to_tif(path_to_spools+spool_file+'/'+dat, path_to_tifs, [str(count), str(count+1), str(count+2)])
        count += 3
    #print(f'Processing {count} from file:\nt\t{spool_file}') 
    #print(f"Trying to access {path_to_spools+spool_file}")
    #dat_to_tif(path_to_spools+spool_file, path_to_tifs, [str(count), str(count+1), str(count+2)])
    
            
cur_spool += index

# Store the new spool number
with open(path_to_log + spool_log_name, 'w') as spool_log:
    print(f"writing new spool num {cur_spool-1}")    
    spool_log.write(str(cur_spool-1))

tif_dir_entries = [i for i in os.listdir(path_to_tifs) if i.endswith('.tif')]
tifs_seq = sorted(tif_dir_entries, key = lambda n : int(n[:-4]))

for index in range(len(scan_log.data.index.values)):
    print(f'Processing {index}/{len(tifs_seq)}')
    tif_data = np.array(Image.open(path_to_tifs+str(index)+'.tif'), dtype=np.uint16)
    if index==1:
        col = tif_data[:, len(tif_data[0])//2]
        plt.plot(col)
        plt.show()
        ifft_dif = fftshift(ifft(ifftshift(col)))
        plt.subplots(1,2)
        plt.subplot(1,2,1)
        plt.plot(abs(ifft_dif)**2, 'o-')
        plt.subplot(1,2,2)
        plt.plot(np.unwrap(np.angle(ifft_dif)), 'o-')
        plt.show()
    


"""
# Get absorption data
# First define parameters
thickness = 5E-6 # metres

fname = './HenkeTables/Fe.txt'
data  = np.genfromtxt(fname, delimiter='  ', skip_header=2).transpose()
energy, delta, beta = data

energy_p = np.linspace(energy[0], energy[-1], 1000)
delta_p, beta_p  = interp_delta_beta(energy_p, energy, delta, beta)

#trans = transmission(energy_p, delta_p, beta_p, thickness)

#plt.plot(energy_p, np.sqrt(np.real(trans)**2 + np.imag(trans)**2) / constants['eV'])
#plt.show()
ics = []
for index in range(len(scan_log.data.index.values)):
    print(f'Processing {index}/{len(tifs_seq)}')
    tif_data = np.array(Image.open(path_to_tifs+str(index)+'.tif'), dtype=np.uint16)
    ics.append(np.sum(tif_data))

ics = np.array(ics)

plt.subplots(3,1)
plt.subplot(3,1,1)

plt.plot(ics)
plt.title('Integrated Counts (IC)')

plt.subplot(3,1,2)
plt.plot(scan_log.data['Ibs'])
plt.title('Ibs')

plt.subplot(3,1,3)
plt.plot(ics / scan_log.data['Ibs'])
plt.title('IC/Ibs')

plt.show()
"""


#print(sorted(os.listdir(path_to_tifs), key n:))




"""
spool_list = sorted(list_subspools(fpath_to_energy_spools), key=lambda n : int(n[n.find(s)+len(s):-4]))[last_spool:]

    print(spool_list)

    count = (3*last_spool)
    
    for (index, spool_file) in enumerate(spool_list, 1):
            print(f'Processing {count}...') 
            dat_to_tif(spool_file, path_to_tifs, [str(count), str(count+1), str(count+2)])
            count += 3
            
    last_spool += index
    return last_spool-1

"""
#recon_frame_energy()