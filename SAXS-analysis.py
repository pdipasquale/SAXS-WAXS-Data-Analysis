# This code should run some real-time analysis of the data from any experiment we perform at the SAXS/WAXS beamline (or any beamline for that matter). #
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
# The steps required for analysis are listed below. Each step is separated by a section, with an explanation on what needs to be done for analysis. #
# Dat2Tif #
# Convert raw image files into .tif for ease of import and analysis. #


# Reformat Log Files #
# Read in log files and reformat them to something actually readable, with headers and split the log file if necessary. place these reformatted files into a new file. #

    ## Maybe we don't need the log file reformatting step.

# Below extracts the variable name and corresponding value
# For the time being I0 is all we want, find where that occurs and plot that
# We can just change the desired column in the moment, and also just list out what column corresponds to whatever motor position we want to look at

biglog = open("livelogfile.log", 'r')
contents = biglog.readlines()

num_lines2 = len(contents)
print(["Number of lines:", str(num_lines2)])
#rows = list(range(0, num_lines2-1))
rows = list(range(0, num_lines2-1))

I0 = list(range(0, num_lines2-1))
for row in rows:
    row_n = contents[row]
    split_lines = row_n.split(" ")
    I0_list = str(split_lines[20])
    I0_str = (I0_list.split('"'))
    I0[row] = I0_str[1]

plt.plot(rows[1:100], I0[1:100]) # only plotting the first 100 lines becuase there are way too many in the log file
plt.show()

# ---------------------------------------------- #
## Need to import an image, the code for this is below:
## Open image
#file = 'image_file.tif'
#im = Image.open(file)

## Make into Numpy array
#na = np.array(im)
# ---------------------------------------------- #

# DarkField correction. #
# Subtract the dark field images from the frames with the same exposure times. #

    # read in dark field tiffs
        # use the image import code
    # read in diffraction pattern tiffs
        # use the image import code

# Integrated intensity plot #
# Plot the integrated intensity of each of the diffraction images against energy, overplot I0 and separately plot the ratio of intensities (I/I0) #

    # read in DF corrected tiffs, sum the entire screen and save that value in an array. loop through, keep it oer frame at first, sort out energy stuff later.

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
