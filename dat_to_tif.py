import numpy as np
from imageio import imwrite
def dat_to_tif(path_in, path_out, fnames, dim=2048):      
    """
    Converts and saves a .dat file into a series of .tif images.

    Data from the SAXS/WAXS beamline is saved in a .dat format, comprised of 
    multiple measurements. This function extracts the data for each measurement 
    and saves it as a .tif image.
    If converting an entire directory, consider dat_from_file.py instead.

    path_in: 
        The path of the incoming .dat file, including its location and name,
        i.e. './SpoolData1.dat'
    path_out:
        The location to save the converted tifs; this should be a directory
    fnames:
        A list of names to use for each tif. If there are three tifs per dat, 
        this could be ['1','2','3']
    dim:
        The height/width of an image in pixels; at SAXS/WAXS this is usually 2048

    ---------------------------------------------------------------------------

    Author: Jake J. Rogers, La Trobe University
    Date: 6th of September, 2022
    """
    datfile = np.fromfile(path_in, dtype=np.int16)

    for (index, name) in enumerate(fnames):
        imwrite(
            path_out + '/' + name + '.tif',
            datfile[index*dim**2:(index+1)*dim**2].reshape(dim,dim)
        )