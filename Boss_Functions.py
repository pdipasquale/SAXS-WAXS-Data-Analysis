# Anytime we need a new function for analysis just plop it into here
# We will use this file to contain all of our functions for analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dat_to_tif import dat_to_tif
from PIL import Image
import os
from scipy.fft import ifft, ifftshift, fftshift
import datetime
import json
from alive_progress import alive_bar

# Contained within the github file directory; unlikely to change
#fpath_to_dir = 'Z:/Cycle_2024_1/Tran_21019/'
# Due to size, this is contained locally; same data contained in lab computer
#fpath_to_energy_spools = 'FeFF_WhitefieldIonChamberEnergyScan_Att0_24042024_4_tenflux4/'
#fpath_to_time_spools = 'FeFF_WhitefieldIonChamberTimeScan_Att0_24042024_4_tenflux4/'

class Logfile:
    def __init__(self, fpath, fname_key = "chanh_filename", stop=-1):
        self.data = pd.read_json(fpath, lines=True).iloc[:stop]        
        self.fname_key = fname_key

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

    
#    def wfdf(self, key=None):
#        df = self.data
#        if key is None:
#           return df.loc[ (df['chanh_filename'].str.contains('dark') or (df['chanh_filename'].str.contains('thru'))) ]
#        
#        return df.loc[ (df['chanh_filename'].str.contains('dark') or (df['chanh_filename'].str.contains('thru'))), key]
    
def unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def load_tif(tif_dir, tif_name):
    return np.array(Image.open(tif_dir+tif_name), np.uint16)



# Performs the integrated counts for a given log object
# Start and stop are particularly helpful for real time analysis
def integrated_count(tif_dir, dataframe, start=0, stop=-1):
    print(f"Performing integrated count. Beginning from {start}.tif")
    ics = [] 

    span = enumerate(dataframe.index.values[start:stop], start)

    with alive_bar(int(stop-start)) as bar:
        for (count, value) in span:
            print(f"processing {value}.tif")
            if count%100 == 0:
                print(f'{count/len(dataframe.index.values[start:stop])*100}%')

            raw = np.array(load_tif(tif_dir, str(value) + '.tif'), np.uint16)          
            """
            col = np.argmax(np.max(raw, axis=0))            
            print(f'max col = {col}')
            ics.append(np.average(raw[: , np.max((col - 200, 0)) : np.min((col + 200, len(raw[0])-1 ))]))
            

            """
            # THIS METHOD SELECTS THE COLUMN WITH PEAK VALUE
            #df_corr = raw - np.mean(raw[1848:2047, 0:200])            
            dark = np.average(raw[len(raw[0])-200:len(raw[0]),len(raw[0])-200:len(raw[0])])                        

            col = np.argmax(np.max(raw, axis=0))            

            ics.append(np.average(raw[:, col]) - dark)
            
            bar()

    return ics

# Returns the averaged dark frame as a 2D array 
# and also the dark current
def add_dark_correction(log):   
    dc = np.average(log.loc[log['chanh_filename'].str.contains('dark'), 'Ibs'].values)    
    # Ask Chanh about negative and zero values
    cor = np.array(log['Ibs']) - dc * np.array(log['chanh_exp_time'].values)
    log['IbsCorrected'] = np.fmax(cor, np.ones(cor.shape))
    
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

# New idea for extracting the tif files for the real time calculation of the integrated counts;

# write the tifs to a file; 'converted_tifs' in the Tran21019/analysis folder, use a try & catch
# to read a .txt file in the respective 'converted_tifs' folders which contains purely the number
# of already converted tifs. If there is no text file then it will create one and set it to '0'.
# it will read the int in the .txt and skip creating that many of the tifs, only creating the new
# ones and updating the integer.

#This is now done. results are below. function testing being done in the window to the right
def spool_logger(path_to_log):
    logname = "spool_num.txt"    
    if logname not in os.listdir(path_to_log):
        # Create it
        cur_spool = 0
        with open(path_to_log + logname, 'w') as spool_log:
            print("spool_num.txt not found, starting a new log at 0")
            spool_log.write(str(cur_spool))
    else:
        with open(path_to_log + logname, 'r') as spool_log:
            
            cur_spool = int(spool_log.readline().strip())
            print("spool_num.txt found, reading the last spool number:" + str(cur_spool))
            
    return cur_spool

def spool_relogger(path_to_log, cur_spool):
    logname = "spool_num.txt"
    with open(path_to_log + logname, 'w') as spool_log:
            print("writing most recent spool: " + str(cur_spool) + " to log")
            spool_log.write(str(cur_spool-1))

def list_subfiles(dir):
    arr = []
    for rootpath, subdirs, files in os.walk(dir):
        for file in files:
            arr.append(rootpath+'/'+file)
                
    return arr

def list_subspools(dir):
    print(f'dir is {dir}')
    return [i for i in list_subfiles(dir) if 'Spool' in i]    

def extract_frames_from_spool(fpath_to_energy_spools, last_spool, path_to_tifs): # also should probably check to change to change variable name to just fpath_to_spools if works for the time scans too

    # check if the following if argument works, other wise find another way to check if the folder exists, same for the later if else that creates the scan directory in the converted_tifs folder
    #spool_dirs = [fpath_to_energy_spools + dir + '/' for dir in os.listdir(fpath_to_energy_spools) if 'Spool' in dir]

    #tifnum = -1 # Initialise as a unique value non-accidentally replicable value

    # Already changed dat_to_tif to output to the converted_tifs folder, but need to change the following to start from the spool indexed by tifnum
    # or which ever is the first non-converted frame. then go up to the last spool (maybe figure out how to do it in a way where it can potentially
    # work around unfilled spools).


    print(f"Last processed Spool{last_spool}")

    #print(f'extract from {fpath_to_energy_spools}')

    s = 'SpoolData'
    
    # key=lambda n : int(n[len(s):-4])

    spool_list = sorted(list_subspools(fpath_to_energy_spools), key=lambda n : int(n[n.find(s)+len(s):-4]))[last_spool:]

    if spool_list == []:
        print("Spool list empty!")
        return

    count = (3*last_spool)
    with alive_bar(len(spool_list)) as bar:
        for (index, spool_file) in enumerate(spool_list, 1):
                print(f'Processing spool: {index} of {len(spool_list)}from:\nt\t{spool_file}...') 
                dat_to_tif(spool_file, path_to_tifs, [str(count), str(count+1), str(count+2)])
                count += 3
                bar()
        last_spool += index
        
        # Return the last spool-1 and the last tif number, to adjust for dead frames
        return (last_spool-1, 3*(last_spool-1))



def process_frame_data(fpath, file_names, frames_per_energy=10):
    data = []
    for index, frame in enumerate(os.listdir(fpath)):
        if index >= len(file_names):
            return np.array(data)
        if 'dark' not in file_names[index]:
            data.append(np.average(np.asarray(Image.open(fpath+frame, 'r')), axis=1))
            
    return np.array(data)

# fEED IN COLumn fom dataframe that give file names
def without_darkf(dist, file_names):
    return dist[np.vectorize(lambda s: 'dark' not in s)(file_names)]

def maxnorm(dist):
    return dist/np.max(dist)

def plot_sums(tif_dir, energy_array, Ibs_array):
    tifnames = [i for i in list_subfiles(tif_dir) if 'spool_num' not in i]
    summed_frames = []
    real_energy = []
    real_ibs = []
    c = 0
    #load in tiff data
    with alive_bar(len(tifnames)) as bar:

        for tifname in sorted(tifnames):
            frame = np.asarray(Image.open(tifname, 'r'))
            recon1d =  fftshift(ifft(ifftshift(np.mean(frame, axis=1))))
            summed_frames.append(max(abs(recon1d)))
            real_energy.append(energy_array[c])
            real_ibs.append(Ibs_array[c])
            c =+ 1
            bar()
    plt.plot(real_energy, np.divide(summed_frames, real_ibs))
    plt.show()

def recon_single_frame(tiff_full_location, alignment_flag):
    print(alignment_flag)
    print("alignment not implemented yet")
    
    #load in tiff data
    frame = np.asarray(Image.open(tiff_full_location, 'r'))
    #frame_1d = np.mean(frame, axis=1) # axis 1 sums along the right
    frame_1d = frame[:, len(frame[0])//2]
    recon1 = fftshift(ifft(ifftshift(frame_1d)))
    plt.plot(np.sqrt(np.real(recon1)**2 + np.imag(recon1)**2))
    plt.show()
    phase1 = np.angle(recon1)
    plt.plot(phase1)
    plt.show()


def recon_frame_energy(tif_dir, filter_log, phase_roi):
    print("alignment not implemented yet")
    
    #tifnames = [i for i in list_subfiles(tif_dir) if str(i).endswith('.tif')]
    absorption = []
    phase = []
    raw_I = []
    raw_I_on_Ibs = []

    with alive_bar(len(filter_log.index)) as bar:
        for index, ibs in zip(filter_log.index, filter_log['Ibs']):            
            temp = Image.open(tif_dir + str(index)+'.tif', 'r')            
            frame = np.asarray(temp, dtype=np.uint16)
            #df_corr = (frame - np.mean(frame[1600:2048, 1600:2048]))
            #df_corr[df_corr < 0] = 0
            df_corr = frame
            frame_1d = df_corr[:, len(frame)//2] / ibs # centre column
            recon1 = fftshift(ifft(ifftshift(frame_1d)))
            absorption.append(np.max(abs(recon1)))
            raw_I.append(np.sum(frame))
            raw_I_on_Ibs.append(np.sum(frame/ibs))
            unwrap_phase = np.unwrap(np.angle(recon1[1024:]))
            phase_val = np.mean(unwrap_phase[phase_roi-1024])
            phase.append(phase_val)
            bar()

            #if index % 100 == 0:
            #    break     

    return phase, absorption, raw_I, raw_I_on_Ibs

def single_slit(x, width, offset=0):
    return np.where((x-offset)<=(width/2), 1, 0)*np.where((x-offset)>-(width/2), 1, 0)

def partial_slit(x, width1, width2, trans1, trans2, off1=0, off2=0):
    slit1 = trans1*single_slit(x, width1, offset=-width1/2 + off1)
    slit2 = trans2*single_slit(x, width2, offset=width2/2 + off2)
    return slit1 + slit2

def liveLogInterpreter(fileName):

    # Open the log file to be read in
    logFile = open(fileName,"r")

    # Initialise storage arrays
    darkFrames = [] # All of the json objects (as dicts) that are dark frames
    realFrames = [] # All of the json objects (as dicts) that are actual measurements
    darkIndexes = [] # This stores the indexes of the dark frames, needed for the reconstruction process.
    c = 1 # This is the line number

    # Read in the first line to initialise
    currentLine = logFile.readline()

    # Begin to read through the log file line by line
    while currentLine:
    
        # Create the JSON object as a dict
        currentJSON = json.loads(currentLine)

        # Identify any dark frames and add them to darkFrames list, otherwise add to realFrames list
        #darkIndex = currentLine.find('dark')
        #if darkIndex > 0:
        #    darkFrames.append(currentJSON)
        #    darkIndexes.append(c)

#        else:
        realFrames.append(currentJSON)

        # Once the current line has been assigned as a dark frame or not,
        # read in the next line to continue
        currentLine = logFile.readline()
        #c = c+1

    # just a check to see it's working, should print the timestamps of the first and last
    # 'real' (non-dark) frames
    #print(" ")
    #print("Reading in JSON objects test (should be initial and final timestamps followed by number of frames):")
    #print(realFrames[0].get("TimeStamp"))
    #print(realFrames[-1].get("TimeStamp"))
    #print(len(realFrames))
    #print("Indexes of dark frames:")
    #print(" ")
    #print(darkIndexes)
    #print(" ")

    # Close the log file
    logFile.close()

    # in order to be able to plot particular variables with ease; create lists/arrays of
    # desired variables to be plotted;
    v = "Ibs" # This is the key being plotted, change here only
    x = [] # this will be the time axis (in seconds) from the start of measuring
    y = [] # this will be the variable axis
    energy = []
    counter = 0

    # initialise the time axis based on the timestamp
    tstring = realFrames[0].get("TimeStamp")
    tlist = tstring.split(' ') # split the timestamp string into a date and time string
    dstring = tlist[0]
    tstring = tlist[-1]
    
    # split the date string into year, month and day
    dlist = dstring.split('-') 
    yearI = int(dlist[0])
    monthI = int(dlist[1])
    dayI = int(dlist[2])

    # split the time string into hours, minutes and seconds
    tlist = tstring.split(':')
    hoursI = int(tlist[0])
    minutesI = int(tlist[1])
    secondsI = tlist[2]
    secondsL = secondsI.split('.')
    secondsI = int(secondsL[0])
    msecondsI = int(secondsL[1])

    # create the initial time as a datetime object
    tI = datetime.datetime(yearI,monthI,dayI,hoursI,minutesI,secondsI,msecondsI)

    # retreive the desired variable values from the realFrames list
    while counter < len(realFrames):

        # add the relevant value according to the key
        y.append(realFrames[counter].get(v))
        energy.append((realFrames[counter].get("Si111_monochromator_energy")))
        # get the time for the x axis
        time = realFrames[counter].get("TimeStamp")
        tlist = time.split(' ') # split the timestamp string into a date and time string
        dstring = tlist[0]
        tstring = tlist[-1]
    
        # split the date string into year, month and day
        dlist = dstring.split('-') 
        year = int(dlist[0])
        month = int(dlist[1])
        day = int(dlist[2])

        # split the time string into hours, minutes and seconds
        tlist = tstring.split(':')
        hours = int(tlist[0])
        minutes = int(tlist[1])
        seconds = tlist[2]
        secondsL = seconds.split('.')
        seconds = int(secondsL[0])
        mseconds = int(secondsL[1])

        # create the current time datetime object
        tF = datetime.datetime(year,month,day,hours,minutes,seconds,mseconds)

        # need to find the time in seconds from the start of the measuring keeping in mind new days/months etc.
        t = tF-tI # creates t as a timedelta object which calculates the time passage

        xval = t.total_seconds()

        x.append(xval)
        
        counter = counter+1

    # format and display the plot
#    plt.plot(x,y)
#    plt.xlabel('Time (seconds)')
#    plt.ylabel(v)
#    plt.title("Plot of " + v + " in seconds from first measurement")
#    plt.show()
    Ibs_array = y

    return darkIndexes, Ibs_array, energy



def white_field_absorption_corrector(tif_dir, df_idx, white_idx, white_log, whole_log):
    print("alignment not implemented yet")
    
    #tifnames = [i for i in list_subfiles(tif_dir) if str(i).endswith('.tif')]
    raw_I = []
    raw_I_on_Ibs = []

    raw_white = []
    raw_white_on_Ibs = []

    real_Ibs = []
    white_Ibs = []

    #with alive_bar(len(filter_log)) as bar:
    for index, ibs in zip(whole_log.index, whole_log['Ibs']):  
        if index in df_idx or index in white_idx:
            continue
        else:
            temp = Image.open(tif_dir + str(index)+'.tif', 'r')            
            frame = np.asarray(temp, dtype=np.uint16)
            raw_I.append(np.sum(frame))
            raw_I_on_Ibs.append(np.sum(frame/ibs))
            real_Ibs.append(ibs)
        

            #if index % 100 == 0:
            #    break     
    #with alive_bar(len(white_log)) as bar:
    for index, ibs in zip(white_log.index, whole_log['Ibs']):
        if index in white_idx:
            #print("I AM IN WHITE LOGS NOW")
            temp_white = Image.open(tif_dir + str(index)+'.tif', 'r')
            frame_white = np.asarray(temp_white, dtype=np.uint16)
            raw_white.append(np.sum(frame_white))
            raw_white_on_Ibs.append(np.sum(frame_white/ibs))
            white_Ibs.append(ibs)
        else:
            continue
    
    return raw_I, raw_I_on_Ibs, raw_white, raw_white_on_Ibs, real_Ibs, white_Ibs

# 