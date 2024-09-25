function scaled_phase = scaling_spect(Reference,Spectra,eV_min,eV_max)

%   Reference = Reference spectra, Theoretical, or Database (in column);

%   Spectra = Spectra-of-interest

%   eV_min = first point for scaling

%   Higher_En = Second point for scaling

%%

% Checking if eV requested exist on Spectra

test1 = find(Spectra == eV_min, 1);
test2 = find(Spectra == eV_max, 1);

    if isempty(test1) || isempty(test2)
        disp('!! Energy selected does not exist in Spectra !!');
        return;  % Exit the function immediately
    end   
    
% Indexing Reference
pre_ind1 = find(Reference == eV_max, 1);
pre_ind2 = find(Reference == eV_min, 1);

% Interpolate to obtain required eV (min/max)
if isempty(pre_ind1)
    f_max = find(Reference(:,1)<eV_max, 1, 'last');
    m_interp_max = interp1(Reference(:,1),Reference(:,2),eV_max,'linear'); % 2nd kink of FFAST's eV
    Reference = [Reference(1:f_max,:); [eV_max,m_interp_max];  Reference(f_max+1:end,:)];   
end

if isempty(pre_ind2)
    f_min = find(Reference(:,1)<eV_min, 1, 'last');
    m_interp_min = interp1(Reference(:,1),Reference(:,2),eV_min,'linear'); % 2nd kink of FFAST's eV
    Reference = [Reference(1:f_min,:); [eV_min,m_interp_min];  Reference(f_min+1:end,:)];   
end

% Reindexing
ind1 = Reference == eV_max;
ind2 = Reference == eV_min;

y0_min = Reference(ind2,2);
y0_max = Reference(ind1,2);

% Scaling Spectra
ind_ymin = Spectra == eV_max;
ind_ymax = find(Spectra == eV_min);

scaled_phase(:,2) = y0_min + (Spectra(:,2)-Spectra(ind_ymax,2))/(Spectra(ind_ymin,2)-Spectra(ind_ymax,2)) * (y0_max-y0_min);

scaled_phase(:,1) = Spectra(:,1);

end

