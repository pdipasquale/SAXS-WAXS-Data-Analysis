# This code should run some real-time analysis of the data from any experiment we perform at the SAXS/WAXS beamline (or any beamline for that matter). #
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image

spool_directory = '/home/paul/Documents/SAXS-WAXS_test_data/raw/Nigel_Naked_Test2_Fine_run2/spool/SpoolDirectory'
tif_directory = '/home/paul/Documents/SAXS-WAXS_test_data/fout'

# ---------------------------------------------- #
# Need to import an image, the code for this is below:
# Open image
file = tif_directory + '/2.tif'
im = Image.open(file)
data = np.asarray(im)
im.show()
#im = img.imread(file)
#data = np.array(im)
#print(data.dtype)
#print(data.shape)
#print(im.format)
#print(im.size)
#print(im.mode)
#print(im.dtype)
#print(im.shape)
#load_im.show()
# Make into Numpy array
#na = np.ndarray(im)
# ---------------------------------------------- #

#pyplot.imshow(im)

#pyplot.show()