% convert radial / instrument FQ velocities to Earth coordinates
%  following instructions from LinkSys 

% then remove bad (signal to noise) data

% Use PhilEx data to make sure the velocity conversion is correct

clear;
printfig = 1; 
% fpath='/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/flowquest_mfiles/testData/PhilEx/';
% fpathWriteFig = '/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/flowquest_mfiles/';

fpath='/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/flowquest_mfiles/testData/Mendo/';
fpathWriteFig = '/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/flowquest_mfiles/';

load([fpath 'proc/FQ_Mendo_AllvarsV2.mat']);
% FQ.Earth.VE = NaN(size(FQ.InstVel.Vx));
% FQ.Earth.VN = NaN(size(FQ.InstVel.Vx));
% FQ.Earth.VW = NaN(size(FQ.InstVel.Vx));

itest = 1564; % for mendo
%itest = 1; % for philex

% test conversion: 

FQ.InstVel.Vx = FQ.InstVel.Vx(1,itest)*1000;
FQ.InstVel.Vy = FQ.InstVel.Vy(1,itest)*1000;
FQ.InstVel.Vz = FQ.InstVel.Vz(1,itest)*1000;

FQ.roll_mean = FQ.roll_mean(itest)
FQ.pitch_mean = FQ.pitch_mean(itest)
FQ.head_mean = FQ.head_mean(itest) %nanmean(FQ.head(:,1))

%for i =1:size(FQ.InstVel.Vx,1)
i=1; 
        Vinst = [FQ.InstVel.Vy(i,:); FQ.InstVel.Vx(i,:); FQ.InstVel.Vz(i,:)] % --> already converted to m/s
        
        %r, p, h stand for roll, pitch and heading respectively - convert to rad
        r = deg2rad(FQ.roll_mean(:))
        p = deg2rad(FQ.pitch_mean(:))
        h = deg2rad(FQ.head_mean(:))
        
        A11 = 1 - sin(r).^2 ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
        A22 = 1 - sin(p).^2 ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
        A33 = sqrt(1- sin(r).^2 - sin(p).^2);
        
        A12 =  sin(r).*sin(p) ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
        A13 =  sin(p);
        A23 = -sin(r);
        
        Rrp(1,1,1:length(A11)) = A11;
        Rrp(1,2,1:length(A11)) = A12;
        Rrp(1,3,1:length(A11)) = A13;
        Rrp(2,1,1:length(A11)) = A12;
        Rrp(2,2,1:length(A11)) = A22;
        Rrp(2,3,1:length(A11)) = A23;
        Rrp(3,1,1:length(A11)) =-A13;
        Rrp(3,2,1:length(A11)) =-A23;
        Rrp(3,3,1:length(A11)) = A33;
            
        Rheading(1,1,1:length(A11)) =  cos(h);
        Rheading(1,2,1:length(A11)) = -sin(h);
        Rheading(1,3,1:length(A11)) =  0;
        Rheading(2,1,1:length(A11)) =  sin(h);
        Rheading(2,2,1:length(A11)) =  cos(h);
        Rheading(2,3,1:length(A11)) =  0;
        Rheading(3,1,1:length(A11)) =  0;
        Rheading(3,2,1:length(A11)) =  0; 
        Rheading(3,3,1:length(A11)) =  1;
           
        %for j=1:size(Vinst,2)
        j=1;
        Srph =      (Rheading(:,:,j) * Rrp(:,:,j));
            Vearth(1:3,j) = Srph * Vinst(:,j)
        %end
        FQ.Earth.VE(i,:) = Vearth(1,:); %North vel
        FQ.Earth.VN(i,:) = Vearth(2,:); %East vel
        FQ.Earth.VW(i,:) = Vearth(3,:); %down vel     
%end

% iBadData = 34:46;
% FQ.Earth.VE(iBadData,:)= NaN;
% FQ.Earth.VN(iBadData,:)= NaN;
% FQ.Earth.Vw(iBadData,:)= NaN;
% 
% save([fpath 'FQ_output_EarthCoords.mat'],'FQ');

if printfig
    figure;
    subplot(221);
    pcolor(FQ.DateNum,repmat(FQ.z,length(FQ.DateNum),1)' ,FQ.Vely);
    caxis([-1 1]*1e-1);
    shading flat; title('Vel y : m/s');
    axdate; axis ij;
    %xlim([datenum(2019,5,16) datenum(2020,10,13)])
    colormap(cbrewer('div','RdBu',24))
    caxis([-1 1]*.5);
    hcbar('Velocity (m/s)',[0.75 0.66 0.1 0.025])
    
    subplot(222);
    pcolor(FQ.DateNum,repmat(FQ.z,length(FQ.DateNum),1)' ,FQ.Earth.VN);
    caxis([-1 1]*1e-1);
    shading flat; title('Earth Vel North : m/s');
    axdate; axis ij;
    %xlim([datenum(2019,5,16) datenum(2020,10,13)])
    colormap(cbrewer('div','RdBu',24))
    caxis([-1 1]*.5);
    
    subplot(223);
    pcolor(FQ.DateNum,repmat(FQ.z,length(FQ.DateNum),1)' ,FQ.Velx);
    caxis([-1 1]*1e-1);
    shading flat; title('Vel x : m/s');
    axdate; axis ij;
    %xlim([datenum(2019,5,16) datenum(2020,10,13)])
    colormap(cbrewer('div','RdBu',24))
    caxis([-1 1]*.5);
    hcbar('Velocity (m/s)',[0.75 0.66 0.1 0.025])
    
    subplot(224);
    pcolor(FQ.DateNum,repmat(FQ.z,length(FQ.DateNum),1)' ,FQ.Earth.VE);
    caxis([-1 1]*1e-1);
    shading flat; title('Earth Vel East : m/s');
    axdate; axis ij;
    %xlim([datenum(2019,5,16) datenum(2020,10,13)])
    colormap(cbrewer('div','RdBu',24))
    caxis([-1 1]*.5);
    %export_fig([fpathWriteFig 'FQVelocityEarth.png'],'-dpng','-r300')
    
%     figure('paperposition',[0 0 7 3]) ; wysiwyg;
%     plot(FQ.DateNum,FQ.xDucerPresDBar)
%     axdate; axis ij;
%     ylabel('pressure - dbar')
%     %export_fig([fpathWriteFig 'FQ_Pressure.png'],'-dpng','-r300')
    
end
