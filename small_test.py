import os

path_in = '/home/paul/Documents/SAXS-WAXS_test_data/raw/Nigel_Naked_Test2_Fine_run2/spool/SpoolDirectory0'
check3 = enumerate(sorted(os.listdir(path_in)), 1)
#idx = 1
c1 = 1
c2 = 2
c3 = 3
tifsperdat = 3
tifs = tifsperdat
index = 0
#print([range(idx,idx+3, 1)])
F = 1
FF = tifsperdat
for (idx, spool) in check3:
    
    print([str((i)) for i in range(F,FF+1)])
    F = F + 3
    FF = FF + 3

#    for F in range(idx, idx+3):
#        Fnum = i*tifsperdat
#        print(str(spool) + ' = ' + str(F))
#    idx = idx+3

