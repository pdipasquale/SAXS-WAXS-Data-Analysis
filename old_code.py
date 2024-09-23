"""
try: 
    os.mkdir(save_dir)
except:
    print("Directory exists.")

try:
    print('Loading absorption and phase arrays.')

    
    with open(save_dir+'absorption.npy', 'rb') as f:
        absorption = np.load(f)

    with open(save_dir+'phase.npy', 'rb') as f:
        phase = np.load(f)

    with open(save_dir+'raw_I.npy', 'rb') as f:
        raw_I = np.load(f)

    with open(save_dir+'raw_I_on_Ibs.npy', 'rb') as f:
        raw_I_on_Ibs = np.load(f)

    with open(save_dir+'raw_white.npy', 'rb') as f:
        raw_white = np.load(f)

    with open(save_dir+'raw_white_on_Ibs.npy', 'rb') as f:
        raw_white_on_Ibs = np.load(f)

    with open(save_dir+'real_Ibs.npy', 'rb') as f:
        real_Ibs = np.load(f)

    with open(save_dir+'white_Ibs.npy', 'rb') as f:
        white_Ibs = np.load(f)





except:
    print('Absorption and phase arrays not found. Calculating...')

    raw_I, raw_I_on_Ibs, raw_white, raw_white_on_Ibs, real_Ibs, white_Ibs = white_field_absorption_corrector(
        path_to_tifs, 
        nodf, 
        phase_roi=1038
    )

    with open(save_dir+'absorption.npy', 'wb') as f:
        np.save(f, absorption)
    with open(save_dir+'phase.npy', 'wb') as f:
        np.save(f, phase)
    with open(save_dir+'raw_I.npy', 'wb') as f:
        np.save(f, raw_I)
    with open(save_dir+'raw_I_on_Ibs.npy', 'wb') as f:
        np.save(f, raw_I_on_Ibs)
    with open(save_dir+'raw_white.npy', 'wb') as f:
        np.save(f, raw_white)
    with open(save_dir+'raw_white_on_Ibs.npy', 'wb') as f:
        np.save(f, raw_white_on_Ibs)
    with open(save_dir+'real_Ibs.npy', 'wb') as f:
        np.save(f, real_Ibs)
    with open(save_dir+'white_Ibs.npy', 'wb') as f:
        np.save(f, white_Ibs)



if len(absorption) < len([i for i in os.listdir(path_to_tifs) if str(i).endswith('.tif')]):
    print('!!Need to process more tifs!!')

    print(f'Already processed: {len(abs
    orption)} tifs')
    print(f'But there are {len(os.listdir(path_to_tifs))-2} tifs i
    n total')

    new_phase, new_absorption, new_raw_I, new_raw_I_on_Ibs = recon_frame_energy(
        path_to_tifs, 
        # -1 for spool file, -1 in case last one is full
        nodf.iloc[len(absorption):len(os.listdir(path_to_tifs))-2,:],        
        phase_roi=1038
    )
    absorption = np.concatenate((absorption, new_absorption))
    phase = np.concatenate((phase, new_phase))
    raw_I = np.concatenate((raw_I, new_raw_I))
    new_raw_I_on_Ibs = np.concatenate((raw_I_on_Ibs, new_raw_I_on_Ibs))
    with open(save_dir+'absorption.npy', 'wb') as f:
        np.save(f, absorption)  
    with open(save_dir+'phase.npy', 'wb') as f:
        np.save(f, phase)
    with open(save_dir+'raw_I.npy', 'wb') as f:
        np.save(f, raw_I)
    with open(save_dir+'raw_I_on_Ibs.npy', 'wb') as f:
        np.save(f, raw_I_on_Ibs)
    with open(save_dir+'raw_I_on_Ibs.npy', 'wb') as f:
        np.save(f, raw_I_on_Ibs)

"""





"""
if len(raw_I) < len([i for i in os.listdir(path_to_tifs) if str(i).endswith('.tif')]):
    print('!!Need to process more tifs!!')

    print(f'Already processed: {len(raw_I)} tifs')
    print(f'But there are {len(os.listdir(path_to_tifs))-2} tifs in total')
        #df_idx, 
        #wf_idx,
        #wf_log,
        #log_energy.data
    new_raw_I, new_raw_I_on_Ibs, new_raw_white, new_raw_white_on_Ibs, new_real_Ibs, new_white_Ibs = white_field_absorption_corrector(
        path_to_tifs,
        df_idx,
        wf_idx,
        wf_log,
        # -1 for spool file, -1 in case last one is full
        nodf[len(raw_I):len(os.listdir(path_to_tifs))-2,:],        
        nowf[len(raw_I):len(os.listdir(path_to_tifs))-2,:]
    )
    #absorption = np.concatenate((absorption, new_absorption))
    #phase = np.concatenate((phase, new_phase))
    raw_I = np.concatenate((raw_I, new_raw_I))
    new_raw_I_on_Ibs = np.concatenate((raw_I_on_Ibs, new_raw_I_on_Ibs))
    raw_white = np.concatenate((raw_white, new_raw_white))
    raw_white_on_Ibs = np.concatenate((raw_white_on_Ibs, new_raw_white_on_Ibs))
    real_Ibs = np.concatenate((real_Ibs, new_real_Ibs))
    white_Ibs = np.concatenate((white_Ibs, new_white_Ibs))

#    with open(save_dir+'absorption.npy', 'wb') as f:
#        np.save(f, absorption)
#    with open(save_dir+'phase.npy', 'wb') as f:
#        np.save(f, phase)
    with open(save_dir+'raw_I.npy', 'wb') as f:
        np.save(f, raw_I)
    with open(save_dir+'raw_I_on_Ibs.npy', 'wb') as f:
        np.save(f, raw_I_on_Ibs)
    with open(save_dir+'raw_white.npy', 'wb') as f:
        np.save(f, raw_white)
    with open(save_dir+'raw_white_on_Ibs.npy', 'wb') as f:
        np.save(f, raw_white_on_Ibs)
    with open(save_dir+'real_Ibs.npy', 'wb') as f:
        np.save(f, real_Ibs)
    with open(save_dir+'white_Ibs.npy', 'wb') as f:
        np.save(f, white_Ibs)
"""