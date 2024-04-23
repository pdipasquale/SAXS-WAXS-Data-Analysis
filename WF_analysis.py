import json
import numpy as np
from scipy.fft import *
from alignment import align1D
import matplotlib.pyplot as plt
import datetime # used to determine timing in experiment
import os # this is required for the reconstruction function
from progress.bar import Bar
from PierceCode import liveLogInterpreter

def white_field_spoolreader(spoolDir, pixdim, scansPerSpool, darkIndexes):

    # First step is to collect all of the spool files data. how many there are as well as retrieving the diffraciton patterns and the frame number.
    # The current plan is to create a 2D data structure with one dimension as the frame number and the other dimension is the diffration pattern.
    # Once that is constructed, a third dimension can be added that will be the energy. Then the average/mean over the frame dimension to reduce down
    # to a 2D data structure of Energy in one dimension and the diffraction pattern in the other (see the reshape() function that Paul mentioned)

    # Collect all frames, taking into consideration files that are subject to the spooling structure, the last .dat file may be empty or only 1 or 
    # 2 scans, so need to adjust for the last .dat file to be able to take a different number of scans. Use the log file as reference as every
    # frame measured has a log. also need to omit dark frames from the construction. See daniels code for reading diffraction patterns and stuff from
    # the .dat files.
    sum_2d = []
    # determine the number of spools
    numSpools = 0
    for path, currentDirectory, files in os.walk(spoolDir):
        for file in files:
            if file.startswith("Spool"):
                numSpools+=1

    # refine the paths to the spool directories into a list
    spoolDir = os.listdir(spoolDir)
    spoolList = [word for word in spoolDir if word.startswith('Spool')]

    # now go through and retrieve the diffraction patterns from the spool files, keeping in mind that we want to cut the run time down for the live
    # analysis. So instead of the entire diffraction pattern, we are taking a line across the pattern and creating an array per diffraction pattern
    # which contains the average intensities in a small area of each fringe along one direction. then alignment only needs to be undertaken in one 
    # axis, dramatically cutting down run time.

    # counter to keep track of the current frame number
    fnum = 0
    bar = Bar('Processing', max=numSpools*3)
    for index1 in range(np.shape(spoolList)[0]):

        # need to get the list of files in the sub directories
        spoolFiles = os.listdir(input_dir + spoolList[index1])

        for (index2, name2) in enumerate(spoolFiles):
            
            # designate individual file path
            file = input_dir + spoolList[index1] + '/' + name2

            # read the data from the file. the data was written to the file with the tofile() function, so use the fromfile() function to retrieve it
            data = np.fromfile(file, dtype=np.int16)

            for index3 in range(scansPerSpool):

                # in this branch we dissect the data retreived from the file, making checks for any empty or darkfield scans and omitting them from
                # the reconstruction process
                real_frame = 0
                if fnum+1 in darkIndexes: # darkIndexes move to global?? need to get the indexes from log interpreter function.

                    # this is where the darkfields are ommited from reconstruction but stored in the dark patterns array

                    dark = data[index3 * pixdim**2:(index3 + 1) * pixdim**2].reshape(pixdim,pixdim)  # convert the data to the 2D pattern
                    #darkPatterns.append(dark) # store the pattern

                else:
                    
                    # this is where the diffraction patterns are retrieved, where the slice is taken and then the reconstruction is applied

                    diff = data[index3 * pixdim**2:(index3 + 1) * pixdim**2].reshape(pixdim,pixdim) # convert the data to the 2D pattern
                    df_corr = (diff - np.mean(diff[0:100, 0:100])) #Dark field correction
                    df_corr[df_corr<0] = 0
                    sum_2d.append(np.sum(df_corr))
                    
                real_frame+=1
                fnum+=1
                
                bar.next()
    bar.finish()                
    return sum_2d

input_dir = "D:/SynchrotronImages/18771b/Cu_Sample1_8879_9679_5s_15f_220922_0256_att3/spool/"
pix_dim = 2048
scansPerSpool = 3
log_dir = "D:/SynchrotronImages/18771b/Cu_Sample1_8879_9679_5s_15f_220922_0256_att3/scatterbrain/livelogfile.json"

dark_indexes, Ibs, energy = liveLogInterpreter(log_dir)
white_field_array = white_field_spoolreader(input_dir, pix_dim, scansPerSpool, dark_indexes)

plt.plot(energy, white_field_array)
plt.show()