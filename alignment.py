## Paul to write up the code for the alignment, in 1D or in 2D maybe with a flag
## The package required to run this is: pip install scikit-image==0.18.1
import time
import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.registration import phase_cross_correlation
from skimage.registration._phase_cross_correlation import _upsampled_dft
from scipy.ndimage import fourier_shift


def gaussian(x, mu, sig):
    """mu is the centre, sig is the FWHM"""
    return (
         1.0 / (np.sqrt(2.0 * np.pi) * sig) * np.exp(-np.power((x - mu) / sig, 2.0) / 2)
     )

# def makeGaussian(size, fwhm, center):
#     """ Make a square gaussian kernel.

#     size is the length of a side of the square
#     fwhm is full-width-half-maximum, which
#     can be thought of as an effective radius.
#     """

#     x = np.arange(0, size, 1, float)
#     y = x[:,np.newaxis]

#     if center is None:
#         x0 = y0 = size // 2
#     else:
#         x0 = center[0]
#         y0 = center[1]

#     return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)

def align1D(ref1D, offset_image1D):

    #x_array = np.linspace(-1024, 1024, 2048) # test array for 1D
    #gauss1D = gaussian(x_array, 0, 200)
    #gauss1D_OS = gaussian(x_array, 13.32, 200)

    #image1D = gauss1D
    #shift1D = 13.71
    #offset_image1D = gauss1D_OS

    shift1D, error1D, diffphase1D = phase_cross_correlation(ref1D, offset_image1D)
    print(f'Detected 1D pixel offset {shift1D}')

    # subpixel precision
    shift1D_sub, error, diffphase = phase_cross_correlation(ref1D, offset_image1D, upsample_factor=100)
    print(f'Detected 1D pixel offset {shift1D_sub}')
    shift1D_sub_round = round(float(shift1D_sub))
    # numpy.multiply
    if shift1D < 0:
        ez_crop = offset_image1D[int(abs(shift1D_sub_round)):-1]
    else:
        ez_crop = offset_image1D[0:-int(shift1D_sub_round)]

    # I need to finish adapting the next line to work properly in python :/
    # g = np.ifft( np.multiply( np.fft(offset_image1D), np.exp( 1i*2*pi*(deltar*Nr/nr) ) ) ) #.*np.exp(-1i*diffphase);
    
    return shift1D, ez_crop

x_array = np.linspace(-1024, 1024, 2048) # test array for 1D

gauss1D = gaussian(x_array, 0, 200)
gauss1D_OS = gaussian(x_array, 13.71, 200)

start_time = time.time()

shift1D, ez_crop = align1D(gauss1D, gauss1D_OS)
# plt.plot(x_array[500:1500], gauss1D[500:1500])
# plt.plot(x_array[500:1500], gauss1D_OS[500:1500])
# plt.plot(x_array[500:1500], ez_crop[500:1500])
# plt.show()

finish_time = time.time()

print("--- %s seconds ---" % (finish_time - start_time))

print(f'Detected subpixel offset (y, x): {shift1D}')