import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft, ifftshift, fftshift
from dat_to_tif import dat_to_tif
from PIL import Image
import os

fname = 'SpoolData8.dat'
img_names = [fname[:-4]+'_'+str(i) for i in range(1,4)]
dat_to_tif(fname, '.', img_names)

# Pick one frame at random 
diff_data = np.asarray(Image.open(img_names[0]+'.tif', 'r'))
#plt.imshow(img1)
#plt.show()

# Acquire dark field data
# Assumes a 200x200 pixel window in the upper-left is 
# appropriately characteristic of the darkfield
darkfield_avg = np.average(diff_data[0:200, 0:200])

# Average along the rows
diff_avg = np.average(diff_data, axis=1) - darkfield_avg
plt.plot(diff_avg)
plt.show()

# Reconstruction
reconstructed = fftshift(ifft(ifftshift(diff_avg)))
plt.plot(np.sqrt(np.real(reconstructed)**2 + np.imag(reconstructed)**2))
plt.show()

# Clean up
for img_name in img_names:
    pass
    os.remove(img_name+'.tif')
