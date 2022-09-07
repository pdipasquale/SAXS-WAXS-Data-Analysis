from dat_to_tif import dat_to_tif
import numpy as np
import os
from dat_from_file import dat_from_file

spool_path = '/home/paul/Documents/SAXS-WAXS_test_data/raw/Nigel_Naked_Test2_Fine_run2/spool/SpoolDirectory'

spool_dirs = 8

pathout = '/home/paul/Documents/SAXS-WAXS_test_data/fout'

#spool_dirs_i = np.linspace(0, 8, 9, dtype=int, endpoint=True)
spool_dirs_i = [0, 1, 2, 3, 4, 5, 6, 7, 8]
c1 = 0
c2 = 1
c3 = 3
dir_num = 0
for dir_num in spool_dirs_i:
    #finputname = '/SpoolData' + str(fnum) + '.dat'
    full_path = spool_path + str(dir_num) # + finputname
    #outputs = ['frame' + str(c1), 'frame' + str(c2), 'frame' + str(c3)]
    dat_from_file(full_path, pathout, dim=2048, tifsperdat=3, override=False)

    #c1 = c1 + 3
    #c2 = c2 + 3
    #c3 = c3 + 3
    #if int(repr(fnum)[-1]) == 9:
    #    dir_num = dir_num + 1