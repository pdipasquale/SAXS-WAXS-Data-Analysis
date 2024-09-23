import numpy as np 
from scipy.fft import *
from PIL import Image

import matplotlib.pyplot as plt

fpath = "Y:/THIS_ONE_JAKE/NiFF_3sec_8343eV.tif"

dif_img = np.array(Image.open(fpath), np.uint16)
col = dif_img[:, len(dif_img[0])//2]
plt.plot(col)
plt.show()
ifft_dif = fftshift(ifft(ifftshift(col)))
plt.subplots(1,2)
plt.subplot(1,2,1)
plt.plot(abs(ifft_dif)**2, 'o-')
plt.subplot(1,2,2)
plt.plot(np.unwrap(np.angle(ifft_dif)), 'o-')
plt.show()

