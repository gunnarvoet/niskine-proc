% convert "leveled" instrument FQ velocities to Earth coordinates
%  following instructions from LinkSys in DocsFromLinkSys 

% then remove bad (signal to noise) data

clear;
printfig = 1; 
fpath='/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/fq_converted/';
%fpath='/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/DocsFromLinkSys/';
fpathWriteFig = '/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/flowquest_mfiles/';

load([fpath 'FQ_output.mat']);
FQ.Earth.VE = NaN(size(FQ.InstVel.Vx));
FQ.Earth.VN = NaN(size(FQ.InstVel.Vx));
FQ.Earth.VW = NaN(size(FQ.InstVel.Vx));

for i =1:size(FQ.InstVel.Vx,1)
    %i=23; 
    %E3 135 33 306 0 -36 256 -23 -95 243 -29 -29 236 -3 23 284 15 44 344 27 0 346 20 -13 268 21 -80 251 11 12 196 0 9 229 9 -49 216 14 29 210 6 83 222 -17 67 180 -29 39 187 -13 98 178 10 128 186 7 129 213 6 166 183 6 105 196 15 71 224 1 71 232 -3 38 251 -2 12 256 2 118 228 -16 152 159 -13 69 189 5 69 222 11 117 192 6 87 189 10 37 208 6 138 176 -7 155 164 6 94 189 22 66 43 17 118 149 14 94 -50 -24 472 169 -38 315 451 -60 134 525 -57 173 713 -76 0 0 0 0 0 0 0 0 0 
    %Vinst = [FQ.InstVel.Vx(1,i); FQ.InstVel.Vy(1,i); FQ.InstVel.Vz(1,i)] * 1000;
    %h = deg2rad(FQ.head_mean(23));
     
        Vinst = [FQ.InstVel.Vx(i,:); FQ.InstVel.Vy(i,:); FQ.InstVel.Vz(i,:)]; % --> already converted to m/s
        
        %r, p, h stand for roll, pitch and heading respectively - convert to rad
%         r = deg2rad(FQ.roll_mean(:));
%         p = deg2rad(FQ.pitch_mean(:));
        h = deg2rad(FQ.head_mean(:));
        
%         Vinst = [89  -663  -46];
%         h = 247.8 *pi/180; 
        
%         A11 = 1 - sin(r).^2 ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
%         A22 = 1 - sin(p).^2 ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
%         A33 = sqrt(1- sin(r).^2 - sin(p).^2);
%         
%         A12 = sin(r).*sin(p) ./ (sin(r).^2 + sin(p).^2) .* (1 - sqrt(1- sin(r).^2 - sin(p).^2));
%         A13 = sin(p);
%         A23 = -sin(r);
%         
%         Rrp(1,1,1:length(A11)) = A11;
%         Rrp(1,2,1:length(A11)) = A12;
%         Rrp(1,3,1:length(A11)) = A13;
%         Rrp(2,1,1:length(A11)) = A12;
%         Rrp(2,2,1:length(A11)) = A22;
%         Rrp(2,3,1:length(A11)) = A23;
%         Rrp(3,1,1:length(A11)) =-A13;
%         Rrp(3,2,1:length(A11)) =-A23;
%         Rrp(3,3,1:length(A11)) = A33;
            
        Rheading(1,1,1:length(h)) = cos(h);
        Rheading(1,2,1:length(h)) = -sin(h);
        Rheading(1,3,1:length(h)) = 0;
        Rheading(2,1,1:length(h)) = sin(h);
        Rheading(2,2,1:length(h)) = cos(h);
        Rheading(2,3,1:length(h)) = 0;
        Rheading(3,1,1:length(h)) = 0;
        Rheading(3,2,1:length(h)) = 0; 
        Rheading(3,3,1:length(h)) = 1;
           
        for j=1:size(Vinst,2)
            Srph =      (Rheading(:,:,j)); % * Rrp(:,:,j));
            Vearth(1:3,j) = Srph * Vinst(:,j);
        end
        FQ.Earth.VN(i,:) = Vearth(1,:);
        FQ.Earth.VE(i,:) = Vearth(2,:);
        FQ.Earth.VW(i,:) = Vearth(3,:);   
        
        % correct for declination
        
        % Earth coordinates not calculated yet -- see FQ_ConvertInstrument2Earth.m
        
        %rotating u an v velocities to convert from mag. to true directions.
        Uu=FQ.Earth.VE;
        Vv=FQ.Earth.VN;
        
        [Tha,Rha]=cart2pol(Uu,Vv);
        FQdeg=rad2deg(Tha);
        FQdegCor=FQdeg+FQ.declination;
        ThaCorr=deg2rad(FQdegCor);
        [Uua,Vva]=pol2cart(ThaCorr,Rha);
        
        FQ.Velx=Uua;
        FQ.Vely=Vva;

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
