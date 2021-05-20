% convert radial / instrument FQ velocities to Earth coordinates
%  following instructions from LinkSys 

% then remove bad (signal to noise) data

clear;
printfig = 1; 
fpath='/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/fq_converted/';
fpathWriteFig = '/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/flowquest_mfiles/';

load([fpath 'FQ_output.mat']);
FQ.Earth.VE = NaN(size(FQ.InstVel.Vx));
FQ.Earth.VN = NaN(size(FQ.InstVel.Vx));
FQ.Earth.VW = NaN(size(FQ.InstVel.Vx));

for i =1:size(FQ.InstVel.Vx,1)
        Vinst = [FQ.InstVel.Vx(i,:); FQ.InstVel.Vy(i,:); FQ.InstVel.Vz(i,:)]; % --> already converted to m/s
        
        %r, p, h stand for roll, pitch and heading respectively - convert to rad
        r = deg2rad(FQ.roll_mean(:));
        p = deg2rad(FQ.pitch_mean(:));
        h = deg2rad(FQ.head_mean(:));
        A11 = 1 - sin(r).^2 ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
        A22 = 1 - sin(p).^2 ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
        A33 = sqrt(1- sin(r).^2 - sin(p).^2);
        
        A12 = sin(r).*sin(p) ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
        A13 = sin(p);
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
            
        Rheading(1,1,1:length(A11)) = cos(h);
        Rheading(1,2,1:length(A11)) = -sin(h);
        Rheading(1,3,1:length(A11)) = 0;
        Rheading(2,1,1:length(A11)) = sin(h);
        Rheading(2,2,1:length(A11)) = cos(h);
        Rheading(2,3,1:length(A11)) = 0;
        Rheading(3,1,1:length(A11)) = 0;
        Rheading(3,2,1:length(A11)) = 0; 
        Rheading(3,3,1:length(A11)) = 1;
           
        for j=1:size(Vinst,2)
            Srph =      (Rheading(:,:,j) * Rrp(:,:,j));
            Vearth(1:3,j) = Srph * Vinst(:,j);
        end
        FQ.Earth.VE(i,:) = Vearth(1,:);
        FQ.Earth.VN(i,:) = Vearth(2,:);
        FQ.Earth.VW(i,:) = Vearth(3,:);      
end

iBadData = 34:46;
FQ.Earth.VE(iBadData,:)= NaN;
FQ.Earth.VN(iBadData,:)= NaN;
FQ.Earth.Vw(iBadData,:)= NaN;

save([fpath 'FQ_output_EarthCoords.mat'],'FQ');

if printfig
    figure; 
    subplot(211);
    pcolor(FQ.DateNum,repmat(FQ.z,length(FQ.DateNum),1)' + FQ.xDucerPresDBar,FQ.Earth.VE); 
caxis([-1 1]*1e-1);
shading flat; title('east Vel : m/s');
axdate; axis ij; 
xlim([datenum(2019,5,16) datenum(2020,10,13)])
colormap(cbrewer('div','RdBu',24))
caxis([-1 1]*.5); 
hcbar('Velocity (m/s)',[0.75 0.66 0.1 0.025])

subplot(212);
    pcolor(FQ.DateNum,repmat(FQ.z,length(FQ.DateNum),1)' + FQ.xDucerPresDBar,FQ.Earth.VN); 
caxis([-1 1]*1e-1);
shading flat; title('North Vel : m/s');
axdate; axis ij; 
xlim([datenum(2019,5,16) datenum(2020,10,13)])
colormap(cbrewer('div','RdBu',24))
caxis([-1 1]*.5); 

export_fig([fpathWriteFig 'FQVelocityEarth.png'],'-dpng','-r300')

figure('paperposition',[0 0 7 3]) ; wysiwyg;
plot(FQ.DateNum,FQ.xDucerPresDBar)
axdate; axis ij;
ylabel('pressure - dbar')
export_fig([fpathWriteFig 'FQ_Pressure.png'],'-dpng','-r300')

end
