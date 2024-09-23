from Boss_Functions import *
from FraunhofferProp import *
from transmission import transmission, interp_delta_beta
import matplotlib.pyplot as plt
from drawnow import drawnow
import os
#Only need to edit the lines below:

run_name = "NiFF_MainSection2" #Scan name goes here
spool_name = "NiFF_MainSection2"

#-------------------------------------------------------------------------------------------


master_path = "Z:/Cycle_2024_1/Tran_21019/"
master_spools = "Y:/"
path_to_tifs = master_path + "converted_tifs/" + run_name + "/"
path_to_spools = master_spools + spool_name + "/spool/"

path_to_log = path_to_tifs
path_to_json = master_path + run_name + "/scatterbrain/livelogfile.json"

# Reconstruction setup

thickness = 5E-6 # metres

fname = './HenkeTables/Fe.txt'
data  = np.genfromtxt(fname, delimiter='  ', skip_header=2).transpose()
energy, delta, beta = data

energy_p = 7062.55 # Example energy at which to acquire delta, beta
delta_p, beta_p = interp_delta_beta(energy_p, energy, delta, beta)

transcof = transmission(energy_p, delta_p, beta_p, thickness)
# 'raw' x values, scaling dependent upon propagation distance, method, etc.
x = np.arange(-250, 250, 1)
    
dx = 1.4E-6         # in metres
sample_x = dx * x   # x coordinates at the sample plane
slit_width = 10E-6  # in metres
h = 6.62607015E-34
c = 3E8

# wavefunction at the sample plane
plane_wf  = np.ones(x.shape)
gauss_wf  = np.exp(-(1/2)*sample_x**2)
sample_wf = plane_wf * partial_slit(sample_x, slit_width/2, slit_width/2, transcof, 1)

# propagation parameters
wavelength = h*c/energy_p  # in metres
propd = 7    # in metres

# Far field wave function
farfield_wf = fraunhof_prop(sample_wf, wavelength, propd, dx)[0]

# Real time plotting!

#fig, axs = plt.subplots(1, 2)

while True:

    try: 
        os.mkdir(path_to_tifs)
    except:
        print("Directory exists, lets read")
    last_spool = spool_logger(path_to_log)

    #### re-run the spool conversion here:
    last_spool, last_tif_no = extract_frames_from_spool(path_to_spools, last_spool, path_to_tifs)
    #### 
    print(f'path to tifs = {path_to_tifs}')
    print(f'path to json = {path_to_json}')
    spool_relogger(path_to_log, last_spool)
    print("I AM ABOUT TO LOG")
    darkIndexes, Ibs_array, energy_array = liveLogInterpreter(path_to_json)
    print("log file done")


    """
    phase, absorption, real_energy, real_Ibs = recon_frame_energy(
        path_to_tifs, 
        log_energy.no_df('Si111_monochromator_energy').values, 
        log_energy.no_df('Ibs').values
        )

    """
    save_dir = 'Z:/Cycle_2024_1/Tran_21019/analysis/' + run_name + '/'

    try: 
        os.mkdir(save_dir)
        os.mkdir(path_to_tifs)
    except:
        print("Directory exists.")

    ##############################################################################
    #### Jake workng space, 27/04/2024
    ##############################################################################

    # The stop is very important here, otherwise the log file will have more
    # entries than tifs processed during real time analysis.
    log_energy = Logfile(path_to_json, stop=last_tif_no)

    testtifno = log_energy.get_wf().index.values[0]
    """
    test_data = np.array(Image.open(path_to_tifs+str(testtifno)+'.tif'), dtype=np.uint16)
    img = plt.contourf(test_data, levels=50)
    plt.colorbar(img)
    plt.show()
    _ = input('...')
    """
    

    print(f'Log Size = {len(log_energy.data)}')
    print(f'Last tif processed = {last_tif_no}')

    # Leave it up to the user to match the log size with the number of processed 
    # frames
    def ic_load(fname, log):
        try:
            print(f'Attempting to load {fname} -- integrated counts array.')
            with open(save_dir+fname, 'rb') as f:
                ic = np.load(f)
                print(f'Array found. Size: {len(ic)}')
                print(f'In log, found {len(log)} matching entries.')

        except:
            print(f'Could not find {fname} array. Recalculating from 0.')
            
            ic  = integrated_count(path_to_tifs, log, start=0, stop=len(log))
            
            with open(save_dir+fname, 'wb') as f:
                np.save(f, ic)

        # Check that the number of tifs processed matches the length of the 
        # loaded array. If not, add additional entries.   
        # Using tif count instead of log size because the time difference 
        # between tif creation and log file creation leads to mismatches.
        if len(log) > len(ic):
            print(f'More log entries than entries in {fname}. Need to calculate additional integrated counts.')    

            # Redo the last 2 in case of dead frames
            temp = integrated_count(path_to_tifs, log, start=np.max((len(ic)-2, 0)), stop=len(log))
            ic = np.concatenate((ic[:np.max((len(ic)-2, 0))], temp))

            with open(save_dir+fname, 'wb') as f:
                np.save(f, ic)

        return ic

    ic_sample = ic_load('ic_sample.npy', log_energy.get_sample())
    ic_darkf = ic_load('ic_darkf.npy', log_energy.get_df())
    ic_whitef = ic_load('ic_whitef.npy', log_energy.get_wf())

    print(f"IC sample size: {len(ic_sample)}")
    print(f"IC dark field size: {len(ic_darkf)}")
    print(f"IC white field size: {len(ic_whitef)}")

    add_dark_correction(log_energy.data) # Modifies log in-place

    #ic_whitef_ibscor = ic_whitef / (log_energy.data['IbsCorrected'][log_energy.get_wf().index])
    #ic_sample_ibscor = ic_sample / (log_energy.data['IbsCorrected'][log_energy.get_sample().index])

    ic_whitef_ibs = ic_whitef / (log_energy.data['Ibs'][log_energy.get_wf().index])
    ic_sample_ibs = ic_sample / (log_energy.data['Ibs'][log_energy.get_sample().index])

    #plt.plot(log_energy.data['Si111_monochromator_energy'][log_energy.get_sample().index], ic_sample_ibs, 'o-')
    """
    plt.subplots(1,2)
    plt.subplot(1,2,1)
    
    plt.plot(log_energy.get_sample()['Si111_monochromator_energy'][:-2],
             ic_sample_ibs[:-2], 'o-')
    #axs[0].set_xlabel('energy (kev)')
    #axs[0].set_title('IC Sample / Ibs')
    #axs[0].draw()

    
    plt.subplot(1,2,2)
    plt.plot(log_energy.get_wf()['Si111_monochromator_energy'],
             ic_whitef_ibs, 'o-')
    plt.xlabel('energy (kev)')
    plt.title('WF / Ibs')
    """
    def makefig1():        
        plt.figure(1)

        plt.subplot(2,2,1)
        plt.plot(log_energy.get_sample()['Si111_monochromator_energy'][:-2],
            ic_sample_ibs[:-2], 'o-', lw=3)
        plt.xlabel('energy (keV)')
        plt.title('(Sample / Ibs) by energy')

        plt.subplot(2,2,2)
        plt.plot(log_energy.get_wf()['Si111_monochromator_energy'][:-2],
            ic_whitef_ibs[:-2], 'o-', lw=3)
        plt.xlabel('energy (keV)')
        plt.title('WF / Ibs')        

        plt.subplot(2,2,3)
        plt.plot(ic_sample_ibs[:-2], 'o-')        
        plt.xlabel('frame #')
        plt.title('(Sample / Ibs) by frame')
        
        plt.subplot(2,2,4)

        step = 10
        print('calculating average wf')
        avg_wf = np.array([np.sum(ic_whitef_ibs[n:n+step]) for n in range(0, len(ic_whitef_ibs), step)])

        step = 10
        print('calculating average sample')
        avg_sample = np.array([np.sum(ic_sample_ibs[n:n+step]) for n in range(0, len(ic_sample_ibs), step)])

        end_index = np.min((len(avg_wf), len(avg_sample)))

        nth_energy = log_energy.data['Si111_monochromator_energy'][log_energy.get_wf().index][::10]
        
        plt.plot(
        nth_energy[:end_index],
        avg_sample[:end_index] / avg_wf[:end_index], 'ro-')
        plt.xlabel('energy (keV)')
        plt.title('(Sample / WF) by energy')
        
        plt.draw()

        plt.suptitle(f'Real Time Analysis: {last_tif_no} files processed')

        #plt.draw()  # Draw the updated subplots

    drawnow(
        makefig1
    )


    plt.pause(3.0)
    

    #plt.show()