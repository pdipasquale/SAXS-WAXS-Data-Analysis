import numpy as np
import scipy
import matplotlib.pyplot as plt

# This script is for interpolating the energy ranges that we will be using for our scans, specifically to check the spacing and structure that the scan is covering.

def convert_strings_to_floats(input_array):
    output_array = []
    for element in input_array:
        converted_float = float(element)
        output_array.append(converted_float)
    return output_array

# The filenames of the text files containing the reference data are:
# Copper: "XAFS NIMS Database spectra\Cu-K_Cu-foil_Si311_50ms_140625.dat"
# Nickel: "XAFS NIMS Database spectra\Ni-K_Ni-foil_Si311_10ms_131127.dat"
# Iron: "XAFS NIMS Database spectra\Fe-K_Fe-foil_Si111_50ms_120621.dat"

copper_ref = "XAFS NIMS Database spectra/Cu-K_Cu-foil_Si311_50ms_140625.txt"
nickel_ref = "XAFS NIMS Database spectra/Ni-K_Ni-foil_Si311_10ms_131127.txt"
iron_ref = "XAFS NIMS Database spectra/Fe-K_Fe-foil_Si111_50ms_120621.txt"
cobalt_ref = "XAFS NIMS Database spectra/Co-K_Co-foil_Si111_50ms_121117.txt"
# The structure of the reference files is shown below:
# Data starts at row 15
# columns are: Angle, angle, time, 2 (Absorption), 3 (Energy)
# the last two columns are what we need for our interpolation

# Choose your sample below:
sample_dir = copper_ref
edge = 8979
# Put the energy range to evaluate here, it's all calculated relative to the edge
range_eval = np.concatenate((
    np.arange(-20, 0, 3), np.arange(0, 100, 0.5), np.arange(100, 400, 2)
))
print(range_eval)

# Import the XAFS Data
file = open(sample_dir, 'r')
lines = file.readlines()

with open(sample_dir, 'r') as file:
    lines = file.readlines()
    data_array = [line.strip().split() for line in lines]
converted_array = np.array(data_array)
full_array = converted_array.astype(float)

energy = full_array[0:-1, 0]
absorption = full_array[0:-1, 1]

interp_abs = np.interp(range_eval + edge, energy, absorption)

#plt.plot(energy, absorption)
#plt.show()

plt.plot(range_eval, interp_abs)
plt.show()