# This code should run some real-time analysis of the data from any experiment we perform at the SAXS/WAXS beamline (or any beamline for that matter). #
#from tkinter import Frame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

spool_directory = '/home/paul/Documents/SAXS-WAXS_test_data/raw/Nigel_Naked_Test2_Fine_run2/spool/SpoolDirectory'
tif_directory = '/home/paul/Documents/SAXS-WAXS_test_data/fout'

# ---------------------------------------------- #
# Need to import an image, the code for this is below:
# Open image
frame2 = tif_directory + '/2.tif'

#img = mpimg.imread(frame2)
#imgplot = plt.imshow(img)
#plt.show()

img = Image.open(frame2)
img.show() 
# ---------------------------------------------- #

#pyplot.imshow(im)

#pyplot.show()