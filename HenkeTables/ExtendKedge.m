function [New_Energy,New_Spectra] = ExtendKedge(Energy,Spectra,Edge,Interval,Numdata,Type)

% Energy = Energy range 

% Spectra = Abs/Ph spectra

% Edge = Minima in f1, Turning point in f2 (Same SI unit as Energy)

% Interval = Energy interval from Edge (Same SI unit as Energy)

% Numdata = Number of additional datapoint, minimumlly 1

% Type = Input Spectra where 1: Absorption, 2: Phase 
% Abs extends from min/max such that the Edge is the turning point
% Ph extends from one side to Edge and then use the new Edge to complete
% the second half interpolation, i.e, minima
    
    % EXAMPLE - Copper Abs spectra (eV), with new interval of 0.5eV, with
    % additional 3 datapoints
    
    % [New_Energy,New_Spectra] =
    % ExtendKedge(Cu_Energy,Cu_Absorption,K_edge,0.5,3,1);
    
%   Author = T.Kirk 20.08.2024

%% Check the size of the array
[~, n1] = size(Energy);
[~, n2] = size(Spectra);

% If the array is not a column vector, reshape it to a column vector
    if n1 ~= 1
        % Reshape A into a column vector
        Energy = Energy(:);
    end

    if n2 ~= 1
        % Reshape A into a column vector
        Spectra = Spectra(:);
    end

% Check if Energy and Spectra are same dimension;
[m1, ~] = size(Energy);[m2, ~] = size(Spectra);

    if m1 ~= m2
        disp('!! Energy and Spectra size do not match !!');
        return;  % Exit the function immediately
    end   
    
% Check if kedge input falls within range
min_value = min(Energy);
max_value = max(Energy);

is_outside_range = (Edge >= min_value) && (Edge <= max_value);

    if is_outside_range == 0
        disp('!! K-edge input falls outside of Energy range !!');
        return;  % Exit the function immediately
    end  

%% Indexing/Locating Edge
Index = find(Energy == Edge, 1);

% If there is an edge already in the input spectra
    if Index >= 1
        
        new_min_range = Edge-(Interval*Numdata):Interval:Edge-Interval;
        min_interp = interp1(Energy(1:Index,1),Spectra(1:Index,1),new_min_range,'linear'); %
        
        new_max_range = Edge+Interval:Interval:Edge+(Interval*Numdata);
        max_interp = interp1(Energy(Index:end,1),Spectra(Index:end,1),new_max_range,'linear');
        
        New_Energy = [Energy(1:Index-1);new_min_range';Energy(Index);new_max_range';Energy(Index+1:end)];
        New_Spectra = [Spectra(1:Index-1);min_interp';Spectra(Index);max_interp';Spectra(Index+1:end)];
        
        return
        
    end
    
    if Type == 1
        
        % If there is no Edge, find minimum value closest to Edge
        E_min = find(Energy(:,1)<Edge, 1, 'last');
        E_max = find(Energy(:,1)>Edge,1,'first');

        new_min_range = Edge-(Interval*Numdata):Interval:Edge-Interval;
        min_interp = interp1(Energy(1:E_min,1),Spectra(1:E_min,1),new_min_range,'pchip'); % Assuming non-linear relationship

        new_max_range = Edge+Interval:Interval:Edge+(Interval*Numdata);
        max_interp = interp1(Energy(E_max:end,1),Spectra(E_max:end,1),new_max_range,'pchip'); % Assuming non-linear relationship       

        % Temp Energy/Spectra to determine Edge
        temp_Energy = [Energy(1:E_min);new_min_range';new_max_range';Energy(E_min+1:end)];
        temp_Spectra = [Spectra(1:E_min);min_interp';max_interp';Spectra(E_min+1:end)];

        temp_E_min = find(temp_Energy(:,1)<Edge, 1, 'last');
        temp_E_max = find(temp_Energy(:,1)>Edge,1,'first');

        Edge_interp = interp1(temp_Energy,temp_Spectra,Edge,'pchip'); % Assuming non-linear relationship

        New_Energy = [temp_Energy(1:temp_E_min);Edge;temp_Energy(temp_E_max:end)];
        New_Spectra = [temp_Spectra(1:temp_E_min);Edge_interp;temp_Spectra(temp_E_max:end)];
        
    else
        
        % If there is no Edge, find minimum value closest to Edge
        E_min = find(Energy(:,1)<Edge, 1, 'last');
        
        % Determines Pre_Edge + Edge
        new_min_range = Edge-(Interval*Numdata):Interval:Edge;
        min_interp = interp1(Energy(1:E_min,1),Spectra(1:E_min,1),new_min_range,'pchip'); % Assuming non-linear relationship
        
        % Temp Energy/Spectra to determine Edge
        temp_Energy = [Energy(1:E_min);new_min_range';Energy(E_min+1:end)];
        temp_Spectra = [Spectra(1:E_min);min_interp';Spectra(E_min+1:end)];        
        
        Edge_loc = find(temp_Energy == Edge, 1);
        
        new_max_range = Edge+Interval:Interval:Edge+(Interval*Numdata);
        max_interp = interp1(temp_Energy(Edge_loc:end,1),temp_Spectra(Edge_loc:end,1),new_max_range,'pchip'); % Assuming non-linear relationship       
        
        New_Energy = [temp_Energy(1:Edge_loc);new_max_range';temp_Energy(Edge_loc+1:end)];
        New_Spectra = [temp_Spectra(1:Edge_loc);max_interp';temp_Spectra(Edge_loc+1:end)];
        
    end

%% Sorting output (incase your interval exceeds edge-1 or edge+1

[New_Energy,idx]=sort(New_Energy,'ascend');
New_Spectra=New_Spectra(idx);

% Checking repeats
[counts, values] = histcounts(New_Energy, min(New_Energy) : max(New_Energy));
repeatedElements = values(counts >= 2);

%     if ~isempty(repeatedElements)
%         
%         indexes = [];
%         for k = 1 : length(repeatedElements)
%           indexes = [indexes, find(New_Energy == repeatedElements(k))];
%         end
%         disp('!! Check Indexes',{' '},strcat(indexes),{' '},'for repeats !!');
%         return;  % Exit the function immediately
%         
%     end  
    
end
