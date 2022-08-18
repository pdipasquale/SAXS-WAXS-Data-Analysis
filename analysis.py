# This code should run some real-time analysis of the data from any experiment we perform at the SAXS/WAXS beamline (or any beamline for that matter). #
import numpy as np
import matplotlib.pyplot as plt
# The steps required for analysis are listed below. Each step is separated by a section, with an explanation on what needs to be done for analysis. #
# Dat2Tif #
# Convert raw image files into .tif for ease of import and analysis. #


# Reformat Log Files #
# Read in log files and reformat them to something actually readable, with headers and split the log file if necessary. place these reformatted files into a new file. #

biglog = open("livelogfile.log", 'r')
contents = biglog.readlines()
with biglog as fp:
    num_lines = sum(1 for line in fp)

rows = list(range(1, num_lines))
print(rows)
I0 = []
for row in rows:
    row_n = contents[row]
    split_lines = row_n.split(" ")
    I0_str = split_lines[20]
    I0[row] = float(I0_str.split('"')) # value is formatted as "number", need to remove that shit

print(I0)

#row_n = contents[row]
#split_lines = row_1.split(" ")
# Start at 5, 7 because the timestamp format is fucked

# Below extracts the variable name and corresponding value
# For the time being I0 is all we want, find where that occurs and plot that

#lines = list(range(1,len(split_lines)))
#for line in lines:
#	print(line)
#	print(split_lines[line])
# I0 is at line 18/line 20
#I0_str = split_lines[20]
#I0 = I0_str.split('"') # value is formatted as "number", need to remove that shit
#print(float(I0[1]))


# DarkField correction. #
# Subtract the dark field images from the frames with the same exposure times. #


# Integrated intensity plot #
# Plot the integrated intensity of each of the diffraction images against energy, overplot I0 and separately plot the ratio of intensities (I/I0) #


# Reconstruction #
# Reconstruct the CTF of the sample in 1D. Steps are as follows below: #

    # Divide each frame by it's corresponding I0 value #

    # Convert the 2d image to a 1d diffraction pattern. This is either a line down the center, or we crop the image and sum across the x-axis #

    # Take the inverse fourier transform of the diffraction pattern. #

    # The max value, the autocorrelation, will be taken as the value for absorption. Some other analytical steps are required for absolute scaling, but we ignore that for now #

    # The phase will have to be checked manually, but we just take the angle of the complex transmission function and take the average of a pre-defined flat region #
    # ^ this step requires some tweaking, maybe we can find the position that the phase region occurs using a simulation? #

    # The CTF Absorption and Phase should be overplot to show a complete result #


# If anything is wrong we should write some code to quickly overplot absorption and motor values, to diagnose any bad stuff #