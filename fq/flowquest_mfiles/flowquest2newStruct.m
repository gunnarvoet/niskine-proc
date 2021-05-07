%this script reads in the flowquest structure and spits out data in a
%structure similar to the ADCP structures for MC09, also cuts out bad
%data..
%e.g....







%10.6 mag. dec for 







% Vel = 
%                u: [41x16703 double]
%                v: [41x16703 double]
%                w: [41x16703 double]
%            ecAve: [41x16703 double]
%             yday: [1x16703 double]
%          datenum: [16703x1 double]
%                z: [41x1 double]
%     xducer_depth: [1x16703 double]
%                H: [1x16703 double]
%              lat: [1x16703 double]
%              lon: [1x16703 double]
%             temp: [1x16703 double]
%             info: [1x1 struct]
% Vel.info
% ans = 
%         SNadcp: 'SN11181'
%        station: 'LR4'
%         cruise: 'MC09'
%      startyear: 2009
%         mfiles: [1x149 char]
%     processing: [1x63 char]
%          notes: 'mooring was dragged 0.4 nm to NW on 03 Apr 09'

%loading Flowquest data
load(['/volumes/Puao/data_archive/WaveChasers-DataArchive/SamoanPassage/Moorings/sp12/P1/Flowquest/processed/FQ_P1_allvars.mat']);
% FQ = 
%           ensNO: [1x4846 double]
%         DateNum: [1x4846 double]
%            yday: [1x4846 double]
%            Engr: [1x1 struct]
%        NumPings: [1x4846 double]
%       BinLength: [1x4846 double]
%     xDucerDepth: [1x4846 double]
%       roll_mean: [1x4846 double]
%        roll_std: [1x4846 double]
%      pitch_mean: [1x4846 double]
%       pitch_std: [1x4846 double]
%       head_mean: [1x4846 double]
%        head_std: [1x4846 double]
%            roll: [40x4846 double]
%           pitch: [40x4846 double]
%            head: [40x4846 double]
%          RadVel: [1x1 struct]
%         InstVel: [1x1 struct]
%            Vely: [78x4846 double]
%            Velx: [78x4846 double]
%            Velz: [78x4846 double]
%             pgd: [1x1 struct]
%          SigStr: [1x1 struct]
%             SNR: [1x1 struct]
%            Date: {1x4846 cell}
%               z: [1x78 double]
%     Engr_readme: {1x4 cell}
%        rph_info: [1x58 char]
%            info: 'created with Flowquest_text2mat. Vels in m/s'



%PRESENT FORMAT BELOW:


% Vel = 
%                u: [37x23723 double]
%                v: [37x23723 double]
%                w: [37x23723 double]
%            ecAve: [37x23723 double]
%            dtnum: [1x23723 double]
%             yday: [1x23723 double]
%                z: [37x1 double]
%             temp: [1x23723 double]
%     xducer_depth: [1x23723 double]
%         botdepth: 1808
%              lat: 20.589766666666666
%              lon: 1.210241833333333e+02
%       MagDecUsed: 2.566666666666666
%             info: [1x1 struct]

Vel.u=FQ.Velx;
Vel.v=FQ.Vely;
Vel.w=FQ.Velz;
Vel.ec=FQ.SigStr;
Vel.yday=FQ.yday;
Vel.dtnum=FQ.DateNum;
Vel.z=nanmean(FQ.xDucerDepth)+FQ.z; %for downlooker +, uplooker -
Vel.xducer_depth=FQ.xDucerDepth;
%Vel.H=FQ.xDucerDepth;
Vel.lat=-(09+(55.098./60));
Vel.lon=-(169+(44.346./60));
Vel.temp=FQ.Engr.Temp;
Vel.botdepth=5227;
Vel.info.serialNum='Flowquest75';
Vel.info.station='P1';
Vel.info.cruise='SP12';
Vel.info.startyear='2012';
Vel.info.mfiles={'used Flowquest Conv. tool A' ; 'then Flowquest_text2mat.m' ; 'then flowquest2newStruct.m'};
Vel.info.processing={'down-looker, 200 sec ensembles'; '18 pings per. ensemble, 4 s between pings, Declination of 10.6 deg. applied.'};


%cropping bad data:

% Igr=find(Vel.z<(0.14.*nanmean(Vel.xducer_depth)));
% 
% Vel.u(Igr,:)=NaN;
% Vel.v(Igr,:)=NaN;
% Vel.w(Igr,:)=NaN;


%first bin looks bad too

%FOR SP12 P1 mooring
Vel.u(1:2,:)=NaN;
Vel.v(1:2,:)=NaN;
Vel.w(1:2,:)=NaN;

Vel.u(25:end,:)=NaN;
Vel.v(25:end,:)=NaN;
Vel.w(25:end,:)=NaN;


Vel.u(:,1:37)=NaN;
Vel.v(:,1:37)=NaN;
Vel.w(:,1:37)=NaN;




%now removing all bins shallower than the surface.

Isbb=find(Vel.z<0);

Vel.u(Isbb,:)=[];
Vel.v(Isbb,:)=[];
Vel.w(Isbb,:)=[];
Vel.ec.ch0(Isbb,:)=[];
Vel.ec.ch1(Isbb,:)=[];
Vel.ec.ch2(Isbb,:)=[];
Vel.ec.ch3(Isbb,:)=[];
Vel.z(Isbb)=[];

return

%Vel.ec.
%Vel.ec
