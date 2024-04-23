import numpy as np
import matplotlib.pyplot as plt
from transmission import transmission, interp_delta_beta
from FraunhofferProp import fraunhof_prop

def single_slit(x, width, offset=0):
    return np.where((x-offset)<=(width/2), 1, 0)*np.where((x-offset)>-(width/2), 1, 0)

def partial_slit(x, width1, width2, trans1, trans2, off1=0, off2=0):
    slit1 = trans1*single_slit(x, width1, offset=-width1/2 + off1)
    slit2 = trans2*single_slit(x, width2, offset=width2/2 + off2)
    return slit1 + slit2

def amp(f):
    return np.sqrt(np.real(f)**2 + np.imag(f)**2)

def single_slit_min(slitw, wavel, propd, m):    
    return [i*wavel*propd/slitw for i in range(1,m+1)]

def normalise(dist):
    return dist / np.max(dist)
    
thickness = 5E-6 # metres

fname = './HenkeTables/Fe.txt'
data  = np.genfromtxt(fname, delimiter='  ', skip_header=2).transpose()
energy, delta, beta = data

energy_p = 7062.55 # Example energy at which to acquire delta, beta
delta_p, beta_p = interp_delta_beta(energy_p, energy, delta, beta)

transcof = transmission(energy_p, delta_p, beta_p, thickness)
# 'raw' x values, scaling dependent upon propagation distance, method, etc.
x = np.arange(-250, 250, 1)
 
dx = 0.1E-6         # in metres
sample_x = dx * x   # x coordinates at the sample plane
slit_width = 10E-6  # in metres

# wavefunction at the sample plane
plane_wf  = np.ones(x.shape)
gauss_wf  = np.exp(-(1/2)*sample_x**2)
sample_wf = plane_wf * partial_slit(sample_x, slit_width/2, slit_width/2, transcof, 1)

# propagation parameters
wavelength = 1  # in metres
propd = 10    # in metres

# Far field wave function
farfield_wf = fraunhof_prop(sample_wf, wavelength, propd, dx)[0]
fraun_x = wavelength * propd / (len(x) * dx) * x

### Visualisation ###
# Sample plane
plt.subplots(1,2)
plt.suptitle('Sample Plane Wavefield')
plt.subplot(1,2,1)
plt.plot(sample_x, normalise(amp(sample_wf)**2))
plt.xlabel('position (m)')
plt.ylabel('intensity (normalised)')

plt.subplot(1,2,2)
plt.plot(sample_x, np.unwrap(np.angle(sample_wf)))
plt.xlabel('position (m)')
plt.ylabel('phase')
plt.tight_layout()
plt.show()

# Far field
plt.subplots(1,2)
plt.suptitle('Far Field Wavefield')
plt.subplot(1,2,1)
plt.plot(fraun_x, normalise(amp(farfield_wf)**2))
plt.xlabel('position (m)')
plt.ylabel('intensity (normalised)')
ideal_minima = np.array(single_slit_min(slit_width, wavelength, propd, 4))
#plt.plot(ideal_minima, 0*ideal_minima, 'ro')
#print(ideal_minima)

plt.subplot(1,2,2)
plt.plot(fraun_x, np.unwrap(np.angle(farfield_wf)))
plt.xlabel('position (m)')
plt.ylabel('phase')
plt.tight_layout()
plt.show()