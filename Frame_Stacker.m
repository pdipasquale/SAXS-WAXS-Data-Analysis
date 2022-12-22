set_name = ;
input_directory = ;
frames-per-energy = ;
number-of-energies = ;
energy_stacks = zeros(2048, 2048, number-of-energies, number-of-energies);

i = 1;
for E = 1:number-of-energies
	for F = 1:frames-per-energy
		frame_dir = imread(strcat(input_directory, "frame_", num2str(i), ".tif"))
		frame = double(imread(frame_dir));
		energy_stacks(:, :, E, F) = frame;
		
		i = i + 1;
	end



end

save(set_name, energy_stacks)
