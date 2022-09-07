# This code should run some real-time analysis of the data from any experiment we perform at the SAXS/WAXS beamline (or any beamline for that matter). #
#from tkinter import Frame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

def read_tif(fname):
    im = Image.open(fname)
    print('IN: {} [Image size: {}, Image mode: {}]'.format(fname, im.size, im.mode))
    return im

#spool_directory = '/home/paul/Documents/SAXS-WAXS_test_data/raw/Nigel_Naked_Test2_Fine_run2/spool/SpoolDirectory'
#tif_directory = '/home/paul/Documents/SAXS-WAXS_test_data/fout'
tif_directory = './test_frame'
frame2 = tif_directory + '/2.tif'

# ---------------------------------------------- #
# Need to import an image, the code for this is below:
# Open image


#img = mpimg.imread(frame2)
#print(img)
#imgplot = plt.imshow(img)
#plt.show()

#img = Image.open(frame2)
#print(img)
#img.show()
test_frame = read_tif(frame2)
image_array = np.array(test_frame)

print(image_array)
plt.imshow(image_array, cmap='gray')
plt.show()
# ---------------------------------------------- #