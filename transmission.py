import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Written by: Jake J. Rogers
# Date: 19/04/2024

# ALL CONSTANTS ARE IN SI UNITS
constants = {
            'H'  : 6.62607015E-34,   # J
            'eV' : 1.602176634E-19,  # J
            'c'  : 299792458,        # m/s
             }

def transmission(energy, delta, beta, thickness):
    """_summary_

    Args:
        beta (_float_): wave transmission parameter
        delta (_float_): wave transmission parameter
        thickness (_float_): sample thickness
        energy (_float_): in units of keV

    Returns:
        _np.complex_: transmission function
    """
    
    wavelength = constants['H'] * constants['c'] / (energy * constants['eV'])
    
    re_fac = np.exp(-((2*np.pi*beta)/wavelength)*thickness)
    im_fac = np.exp(-1j*((2*np.pi*delta)/wavelength)*thickness)
    
    return re_fac * im_fac


def interp_delta_beta(energy_interp, energy, delta, beta):
    return (np.interp(energy_interp, energy, delta), 
            np.interp(energy_interp, energy, beta))

# TEST RUN
"""
thickness = 5E-6 # metres

fname = './HenkeTables/Fe.txt'
data  = np.genfromtxt(fname, delimiter='  ', skip_header=2).transpose()
energy, delta, beta = data

energy_p = np.linspace(energy[0], energy[-1], 1000)
delta_p, beta_p  = interp_delta_beta(energy_p, energy, delta, beta)

trans = transmission(energy_p, delta_p, beta_p, thickness)

plt.plot(energy_p, np.sqrt(np.real(trans)**2 + np.imag(trans)**2) / constants['eV'])
plt.show()
"""