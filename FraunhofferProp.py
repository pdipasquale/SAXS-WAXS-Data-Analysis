"""
Fraunhofer propagation is complete, meaning all information is
encapsulated within the propagated intensity. Fresnel propagation is NOT.
"""
from scipy.fft import *

import numpy as np
def fraunhof_prop(wf, wavel, z, px):

    N = len(wf)
    n = int(np.floor(N/2))
    L = N*px
    dx2 = wavel*z/L

    x = np.arange(-N/2, N/2, N)        

    [X,Y] = np.meshgrid(x,x)
    R2 = X**2 + Y**2
    pw = wf * np.exp(1j*np.pi*R2/(wavel*z))

    #pw = wf*np.exp(1j*np.pi*R2/(wavel*z))
    return fftshift(fft2(ifftshift(pw)))

#propagated = ff_prop(sample_plane, wavelength, z, px_x)
#cross = propagated[points // 2, :]