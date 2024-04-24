# Template for pulling in and processing data from synchrotron scans
# Writen by: Jake J. Rogers
# Date: 24th of April, 2024

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

fpath = './FeFF/'
for directory in os.listdir(fpath):
    print(directory)
    if 'EnergyScan' in directory:
        df_escan = pd.read_json(fpath+directory+'/scatterbrain/livelogfile.json', lines=True)
    elif 'TimeScan' in directory:
        df_tscan = pd.read_json(fpath+directory+'/scatterbrain/livelogfile.json', lines=True)
        
### Visualisation ###
plt.subplots(2,2, figsize=(15,10))
plt.subplot(2,2,1)
# Numeric time stamp doesn't begin at zero
time_escan = df_escan['NumericTimeStamp']-df_escan['NumericTimeStamp'][0]

plt.plot(time_escan, df_escan['I0'], 'o-')
plt.plot(time_escan, df_escan['Ibs'], 's-')

plt.legend(['I0','Ibs'])
plt.xlabel('Time (s)')
plt.ylabel('Counts')
plt.title('Energy Scan')

plt.subplot(2,2,2)
time_tscan = df_tscan['NumericTimeStamp']-df_tscan['NumericTimeStamp'][0]
plt.plot(time_tscan, df_tscan['I0'], 'o-')
plt.plot(time_tscan, df_tscan['Ibs'], 's-')

plt.xlabel('Time (s)')
plt.ylabel('Counts')
plt.title('Time Scan')

plt.subplot(2,2,3)

plt.plot(time_escan, df_escan['I0']/np.max(df_escan['I0']), 'o-')
plt.plot(time_escan, df_escan['Ibs']/np.max(df_escan['Ibs']), 's-')
plt.xlabel('Time (s)')
plt.ylabel('Counts')
plt.title('Energy Scan (Norm.)')

plt.subplot(2,2,4)
plt.plot(time_tscan, df_tscan['I0']/np.max(df_tscan['I0']), 'o-')
plt.plot(time_tscan, df_tscan['Ibs']/np.max(df_tscan['Ibs']), 's-')

plt.xlabel('Time (s)')
plt.ylabel('Counts')
plt.title('Time Scan (Norm.)')

plt.suptitle(f'Ion Chamber Scan (10% Flux) (7012, 7212, 20eV)')

plt.tight_layout()
plt.show()
