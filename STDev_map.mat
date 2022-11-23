% Input tif location
run_name = '';
images = '/raw_tifs';
tif_dir = strcat([run_name, images, '/']);

load('DFinFo')

% Run details
frames = 20; % frames per energy
total_frames = DF_frames(2) - length(DF_frames);

total_energy = total_frames/frames;

% For loop, loops through each energy and obtains standard deviation map of each set.
i = 1;
for E = 1:total_energy
    for F = 1:frames
        tif_dir = strcat([run_name, images, '/tif', i, '.tif']);
        frame_set(F, :, :) = double(imread(tif_dir));
        i = i + 1        
    end
    
    STDev_maps(E, :, :) = std(frame_set(:, :, :), 1)
  
end
