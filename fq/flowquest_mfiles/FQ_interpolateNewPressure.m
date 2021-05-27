% interpolate the RDI pressure from the LR ADCP nearby to correct the bad
% FQ pressure data

fpath='/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/fq_converted/';
fpathWriteFig = '/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/flowquest_mfiles/';
load([fpath 'FQ_output_EarthCoords.mat']);

lrpath = '/Volumes/Ahua/data_archive/WaveChasers-DataArchive/NISKINE/Moorings/NISKINE19/M2/ADCP/proc/SN10219/';
lrfile = dir([lrpath '*.nc']);

adcp.time = double(ncread([lrpath lrfile.name],'time')); % time in microseconds
%starttime = ncdisp([lrpath lrfile.name],'time')
adcp.dnum = datenum(2019,05,16,09,35,31.965232+(adcp.time/1e6));
adcp.z = ncread([lrpath lrfile.name],'z');
adcp.u = ncread([lrpath lrfile.name],'u')';
adcp.v = ncread([lrpath lrfile.name],'v')';
adcp.temperature = ncread([lrpath lrfile.name],'temperature');
adcp.pressure = ncread([lrpath lrfile.name],'pressure');


figure; 
pcolor(adcp.dnum,adcp.z,adcp.u);
shading flat; 
hold on; axis ij; 
pcolor(FQ.DateNum,repmat(FQ.z,length(FQ.DateNum),1)' + FQ.xDucerPresDBar,FQ.Earth.VE);
caxis([-1 1]*1e-1);
shading flat; title('east Vel : m/s');
axdate; axis ij;
xlim([datenum(2019,5,16) datenum(2020,10,13)])
colormap(cbrewer('div','RdBu',24))
caxis([-1 1]*.5);
hcbar('Velocity (m/s)',[0.75 0.66 0.1 0.025])

ylim([0 2000]); 
