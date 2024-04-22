import numpy as np
import matplotlib.pyplot as plt
from transmission import transmission, interp_delta_beta

def single_slit(x, width):
    return np.where(x<width/2, 1, 0)*np.where(x>-width/2, 1, 0)

thickness = 5E-6 # metres

fname = './HenkeTables/Fe.txt'
data  = np.genfromtxt(fname, delimiter='  ', skip_header=2).transpose()
energy, delta, beta = data

energy_p = 7062.55 # Example energy at which to acquire delta, beta
delta_p, beta_p = interp_delta_beta(energy_p, energy, delta, beta)

x = np.linspace(-1, 1, 1000)

plt.plot(x, single_slit(x, 0.2))
plt.show()