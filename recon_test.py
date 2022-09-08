# This code should run some real-time analysis of the data from any experiment we perform at the SAXS/WAXS beamline (or any beamline for that matter). #
#from tkinter import Frame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from scipy.fft import fft, ifft, ifftshift, fftshift

def read_tif(fname):
    im = Image.open(fname)
    print('IN: {} [Image size: {}, Image mode: {}]'.format(fname, im.size, im.mode))
    return im

#spool_directory = '/home/paul/Documents/SAXS-WAXS_test_data/raw/Nigel_Naked_Test2_Fine_run2/spool/SpoolDirectory'
#tif_directory = '/home/paul/Documents/SAXS-WAXS_test_data/fout'
tif_directory = './test_frame'
frame2 = tif_directory + '/2.tif'
test_frame = read_tif(frame2)
data = np.array(test_frame, dtype='d')
#print(data)
#print(data.dtype)
data2 = np.double(data)

#plt.imshow(image_array)
DF_mean = 300 # fix this!!!
integ = sum(sum(data2[:] - DF_mean))
print(integ)
# DF Correction

# index the middle line of the array for the 1-dimensional cross-section
# one_d = data2[1024, :] # Line through x
one_d = data2[:, 1024] - DF_mean # Line through y
plt.plot(one_d)
plt.show()

# ifft this middle line, angle for phase and abs(max(ifft))^2 for absorption
recon = ifftshift(ifft(one_d))
absorption = np.sqrt(abs(max(recon))*abs(max(recon)))
print(absorption)
phase = np.unwrap(np.angle(recon))

plt.plot(abs(recon))
plt.show()
plt.plot(phase)
plt.show()
# Scan this through energy

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


#print(image_array)
#plt.imshow(image_array, cmap='gray')
#plt.show()
# ---------------------------------------------- #