% interpolate the RDI pressure from the LR ADCP nearby to correct the bad
% FQ pressure data;

% save the final FQ output file :: FQ_InterpolatedFinal.mat in /fq_converted

% AW NOTE: The earth coordinates have not been properly rotated as on 28 May
% 2021, waiting for LinkSys to respond. 

clear
%fpath='/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/fq_converted/';
%fpathWriteFig = '/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/flowquest_mfiles/';
fpath='/Volumes/GoogleDrive/My Drive/research/niskine/data/mooring/niskine-proc/fq/fq_converted/';
fpathWriteFig = '/Volumes/GoogleDrive/My Drive/research/niskine/data/mooring/niskine-proc/fq/flowquest_mfiles/';
load([fpath 'FQ_output_EarthCoords.mat']);

lrpath = '/Volumes/Ahua/data_archive/WaveChasers-DataArchive/NISKINE/Moorings/NISKINE19/M2/ADCP/proc/SN10219/';
lrfile = dir([lrpath 'M2_10219.nc']);

sfpath = '/Volumes/Ahua/data_archive/WaveChasers-DataArchive/NISKINE/Moorings/NISKINE19/M2/ADCP/proc/SN3110/';
sffile = dir([sfpath 'M2_3110.nc']);

figpath = '/Volumes/GoogleDrive/My Drive/research/niskine/data/mooring/niskine-proc/fig/';

adcp.time = double(ncread([lrpath lrfile.name],'time')); % time in microseconds
adcp.dnum = datenum(2019,05,16,09,35,31.965232+(adcp.time/1e6));
adcp.z = ncread([lrpath lrfile.name],'z');
adcp.u = ncread([lrpath lrfile.name],'u')';
adcp.v = ncread([lrpath lrfile.name],'v')';
adcp.temperature = ncread([lrpath lrfile.name],'temperature');
adcp.pressure = ncread([lrpath lrfile.name],'pressure');

adcpsf.time = double(ncread([sfpath sffile.name],'time')); % time in microseconds
adcpsf.dnum = datenum(2019,05,13,0,15,0+(adcpsf.time/1e6));
adcpsf.z = ncread([sfpath sffile.name],'z');
adcpsf.u = ncread([sfpath sffile.name],'u')';
adcpsf.v = ncread([sfpath sffile.name],'v')';
adcpsf.temperature = ncread([sfpath sffile.name],'temperature');
adcpsf.pressure = ncread([sfpath sffile.name],'pressure');

% interpolate the FQ pressure / bins from the LR pressure

% from reading in the raw data from FQ_00_Flowquest_text2mat_NISKINE.m file:  
%  FQ.z=Instdepth+FQ.Engr.BlankDist(1)+BinLength./2+([0:1:(nanmax(NumBins)-1)].*BinLength);

% this is not converting to pressure properly and needs to use a constant
% offset of 306m from teh LR ADCP instead of the FQ xDucerPresDBar
%FQ.xDucerPresDBarFixed = interp1(adcp.dnum,demean(adcp.pressure),FQ.DateNum)+nanmean(FQ.xDucerPresDBar)'; 
%FQ.z2 = ones(size(FQ.z, 2), 1)*FQ.xDucerPresDBarFixed + FQ.z'*ones(1, length(FQ.Date));

% new code: 
FQ.xDucerPresDBarFixed = interp1(adcp.dnum,demean(adcp.pressure),FQ.DateNum)+sw_pres(306,58+57.906/60); 
FQ.z2 = ones(size(FQ.z, 2), 1)*sw_dpth(FQ.xDucerPresDBarFixed',58+57.906/60)' + FQ.z'*ones(1, length(FQ.Date));

FQadcp.u = FQ.Earth.VE;
FQadcp.v = FQ.Earth.VN;
FQadcp.w = FQ.Earth.VW;
FQadcp.z = FQ.z2; 
FQadcp.dnum = ones(size(FQadcp.z, 1), 1)*FQ.DateNum; 

% Plot the M2 full current meter record
figure('paperposition',[0 0 10 6]); wysiwyg;
pcolor(adcp.dnum,adcp.z,sqrt(adcp.u.^2 + adcp.v.^2));
shading flat; 
hold on; axis ij; 
pcolor(adcpsf.dnum,adcpsf.z,sqrt(adcpsf.u.^2 + adcpsf.v.^2));
pcolor(FQadcp.dnum, FQadcp.z, sqrt(FQadcp.u.^2 + FQadcp.v.^2 + FQadcp.w.^2)); shading flat; axis ij;
shading flat; 
axdate; axis ij;
xlim([datenum(2019,5,16) datenum(2020,10,13)])
colormap(cbrewer('seq','YlGnBu',24))
caxis([0 1]*.5);
hcbar('Velocity Amplitude (m/s)',[0.75 0.25 0.1 0.025])
ylim([0 1400]); 
bdr_savefig2(gcf,figpath,'M2_CurrentsFull','p','300','fontsize',10);

% Plot the M2 full current meter record - u
figure('paperposition',[0 0 10 6]); wysiwyg;
pcolor(adcp.dnum,adcp.z,adcp.u);
shading flat; 
hold on; axis ij; 
pcolor(adcpsf.dnum,adcpsf.z,adcpsf.u);
pcolor(FQadcp.dnum, FQadcp.z, FQadcp.u); shading flat; axis ij;
shading flat; 
axdate; axis ij;
xlim([datenum(2019,5,16) datenum(2020,10,13)])
colormap(cbrewer('div','RdBu',24))
caxis([-1 1]*.5);
hcbar('Velocity (m/s)',[0.75 0.25 0.1 0.025])
ylim([0 1400]); 
bdr_savefig2(gcf,figpath,'M2_CurrentsFull_u','p','300','fontsize',10);

% Plot the M2 full current meter record - v
figure('paperposition',[0 0 10 6]); wysiwyg;
pcolor(adcp.dnum,adcp.z,adcp.v);
shading flat; 
hold on; axis ij; 
pcolor(adcpsf.dnum,adcpsf.z,adcpsf.v);
pcolor(FQadcp.dnum, FQadcp.z, FQadcp.v); shading flat; axis ij;
shading flat; 
axdate; axis ij;
xlim([datenum(2019,5,16) datenum(2020,10,13)])
colormap(cbrewer('div','RdBu',24))
caxis([-1 1]*.5);
hcbar('Velocity (m/s)',[0.75 0.25 0.1 0.025])
ylim([0 1400]); 
bdr_savefig2(gcf,figpath,'M2_CurrentsFull_v','p','300','fontsize',10);

% Save new pressure interpolated FQ data
save([fpath 'FQ_InterpolatedFinal.mat'],'FQadcp');

