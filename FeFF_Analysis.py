# Analysis of Ion Chamber readings, including analysis of log files and 
# spool data

# Writen by: Jake J. Rogers
# Date: 24th of April, 2024

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dat_to_tif import dat_to_tif
from PIL import Image
import os

# Contained within the github file directory; unlikely to change
fpath_to_logfiles = './FeFF_IonChamberScan/'
# Due to size, this is contained locally; same data contained in lab computer
fpath_to_energy_spools = '/media/jake/Sony_16GQX/Ion Chamber Testing/Ion Chamber Testing/New folder/FeFF_WhitefieldIonChamberEnergyScan_Att0_24042024_4_tenflux4/spool/'
fpath_to_time_spools = '/media/jake/Sony_16GQX/Ion Chamber Testing/Ion Chamber Testing/New folder/FeFF_WhitefieldIonChamberTimeScan_Att0_24042024_4_tenflux4/spool/'

def read_logfile(fpath):
    for directory in os.listdir(fpath):
        if 'EnergyScan' in directory:
            df_escan = pd.read_json(fpath+directory+'/scatterbrain/livelogfile.json', lines=True)
        elif 'TimeScan' in directory:
            df_tscan = pd.read_json(fpath+directory+'/scatterbrain/livelogfile.json', lines=True)
        
    return (df_escan, df_tscan)

def plot_i0ibs(df_escan, df_tscan):
    plt.subplots(2,2, figsize=(15,10))
    plt.subplot(2,2,1)
    # Numeric time stamp doesn't begin at zero
    time_escan = df_escan['NumericTimeStamp']-df_escan['NumericTimeStamp'][0]

    plt.plot(time_escan, df_escan['I0'], 'o-')
    plt.plot(time_escan, df_escan['Ibs'], 's-')

    plt.legend(['I0','Ibs'])
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Energy Scan')

    plt.subplot(2,2,2)
    time_tscan = df_tscan['NumericTimeStamp']-df_tscan['NumericTimeStamp'][0]
    plt.plot(time_tscan, df_tscan['I0'], 'o-')
    plt.plot(time_tscan, df_tscan['Ibs'], 's-')

    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Time Scan')

    plt.subplot(2,2,3)

    plt.plot(time_escan, df_escan['I0']/np.max(df_escan['I0']), 'o-')
    plt.plot(time_escan, df_escan['Ibs']/np.max(df_escan['Ibs']), 's-')
    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Energy Scan (Norm.)')

    plt.subplot(2,2,4)
    plt.plot(time_tscan, df_tscan['I0']/np.max(df_tscan['I0']), 'o-')
    plt.plot(time_tscan, df_tscan['Ibs']/np.max(df_tscan['Ibs']), 's-')

    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.title('Time Scan (Norm.)')

    plt.suptitle(f'Ion Chamber Scan (10% Flux) (7012, 7212, 20eV)')

    plt.tight_layout()
    plt.show()

def extract_frames_from_spool(fpath):
    frame_dir = fpath+'frames/'
    os.mkdir(frame_dir)
    
    spool_dirs = [fpath+dir+'/' for dir in os.listdir(fpath) if 'Spool' in dir]

    count = 0
    for spool_dir in spool_dirs:
        for (index, spool_file) in enumerate(os.listdir(spool_dir), 1):
            print(f'Processing {count}...')

            dat_to_tif(spool_dir+spool_file, frame_dir, [str(count), str(count+1), str(count+2)])
            count += 3

def process_frame_data(fpath, file_names, frames_per_energy=10):
    data = []
    for index, frame in enumerate(os.listdir(fpath)):
        if index >= len(file_names):
            return np.array(data)
        if 'dark' not in file_names[index]:
            data.append(np.average(np.asarray(Image.open(fpath+frame, 'r')), axis=1))
            
    return np.array(data)

def without_darkf(dist, file_names):
    return dist[np.vectorize(lambda s: 'dark' not in s)(file_names)]

def maxnorm(dist):
    return dist/np.max(dist)

df_escan, df_tscan = read_logfile(fpath_to_logfiles)

# These take a fair amount of time to run, best to run once
#extract_frames_from_spool(fpath_to_spools)
#extract_frames_from_spool(fpath_to_time_spools)

filenames_energy = np.array(df_escan['chanh_filename'], dtype=str)
filenames_time = np.array(df_tscan['chanh_filename'], dtype=str)
"""
print(f'filenames_energy length = {filenames_energy.shape}')
print(f'filenames_time length = {filenames_time.shape}')

frame_data_energy = process_frame_data(fpath_to_energy_spools+'frames/', filenames_energy)
frame_data_time = process_frame_data(fpath_to_time_spools+'frames/', filenames_time)

np.save('./frame_data_energy', frame_data_energy)
np.save('./frame_data_time', frame_data_time)
"""
frame_data_energy = np.load('./frame_data_energy.npy')
frame_data_time = np.load('./frame_data_time.npy')

integrated_counts_energy = np.sum(frame_data_energy, axis=1)
integrated_counts_time = np.sum(frame_data_time, axis=1)

print('withoutdarkf:')
correctedi0 = without_darkf(np.array(df_escan['I0'], dtype=str), filenames_energy)

print(correctedi0)

plt.subplots(1,2)
plt.subplot(1,2,1)

plt.plot(maxnorm(integrated_counts_energy), 'o-')
#plt.plot(maxnorm(integrated_counts_energy/without_darkf(np.array(df_escan['I0'], dtype=str), filenames_energy).astype(int)), 's-')
plt.plot(maxnorm(integrated_counts_energy/without_darkf(np.array(df_escan['Ibs'], dtype=str), filenames_energy).astype(int)), 's-')
plt.plot(maxnorm(without_darkf(np.array(df_escan['Ibs'], dtype=str), filenames_energy).astype(int)), '^-')
plt.ylabel('Counts')
plt.xlabel('Frame #')
plt.title('Integrated Counts Energy Comparison')

plt.legend(['$\int E$', '$\int E / Ibs$', 'Ibs'])

plt.subplot(1,2,2)

plt.plot(maxnorm(integrated_counts_time), 'o-')
plt.plot(maxnorm(integrated_counts_time/without_darkf(np.array(df_tscan['I0'], dtype=str), filenames_time).astype(int)), 's-')
plt.plot(maxnorm(integrated_counts_time/without_darkf(np.array(df_tscan['Ibs'], dtype=str), filenames_time).astype(int)), '^-')

plt.ylabel('Counts')
plt.xlabel('Frame #')
plt.title('Integrated Counts Time Comparison')

plt.tight_layout()
plt.show()
