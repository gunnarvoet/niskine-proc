%loading Flowquest data

load C:\Cruises_Research\PhilEx\FQ_Vels.mat
% % FQ = 
%           ensNO: [1x19561 double]
%         DateNum: [1x19561 double]
%            yday: [1x19561 double]
%            Engr: [1x1 struct]
%        NumPings: [1x19561 double]
%       BinLength: [1x19561 double]
%     xDucerDepth: [1x19561 double]
%       roll_mean: [1x19561 double]
%        roll_std: [1x19561 double]
%      pitch_mean: [1x19561 double]
%       pitch_std: [1x19561 double]
%       head_mean: [1x19561 double]
%        head_std: [1x19561 double]
%            roll: [10x19561 double]
%           pitch: [10x19561 double]
%            head: [10x19561 double]
%          RadVel: [1x1 struct]
%         InstVel: [1x1 struct]
%            Vely: [60x19561 double]
%            Velx: [60x19561 double]
%            Velz: [60x19561 double]
%             pgd: [1x1 struct]
%          SigStr: [1x1 struct]
%             SNR: [1x1 struct]
%            Date: {1x19561 cell}
%               z: [1x60 double]
%     Engr_readme: {'BlankDist is blanking distance in meters'  [1x78 char]  [1x80 char]  [1x72 char]}
%        rph_info: 'roll, pitch, head are values for each ping of the ensemble'
%            info: 'created with Flowquest_text2mat. Vels in m/s'



%loading RDI LR data

load C:\Cruises_Research\PhilEx\ADCP\adcp4021_1.mat

% Vel = 
%           ens_no: [1x21685 double]
%           z_adcp: [1x50 double]
%           p_adcp: [1x50 double]
%         pulselen: 1736
%             yday: [1x21685 double]
%          heading: [1x21685 double]
%            pitch: [1x21685 double]
%             roll: [1x21685 double]
%          hdg_std: [1x21685 double]
%        pitch_std: [1x21685 double]
%         roll_std: [1x21685 double]
%     depth_xducer: [1x21685 double]
%         soundvel: [1x21685 double]
%             temp: [1x21685 double]
%            u_wat: [50x21685 double]
%            v_wat: [50x21685 double]
%            w_wat: [50x21685 double]
%          err_wat: [50x21685 double]
%           ec1_bm: [50x21685 double]
%           ec2_bm: [50x21685 double]
%           ec3_bm: [50x21685 double]
%           ec4_bm: [50x21685 double]
%          cor1_bm: [50x21685 double]
%          cor2_bm: [50x21685 double]
%          cor3_bm: [50x21685 double]
%          cor4_bm: [50x21685 double]
%              pg1: [50x21685 double]
%              pg2: [50x21685 double]
%              pg3: [50x21685 double]
%              pg4: [50x21685 double]

Ivec=[2:1:47];
    fz1=figure;
%set(gca,'position',[.1 .1 0.9 0.9]);
set(fz1,'paperorientation','portrait','paperposition',[0.2500 0.2500 8 10.5000]);




for jj=1:length(Ivec);
jj
    
XwwLR=Vel.u_wat(Ivec(jj),:);
YwwLR=Vel.v_wat(Ivec(jj),:);

XwwFQ=FQ.Velx(Ivec(jj)+1,:);  %for comparable flowquest depths
YwwFQ=FQ.Vely(Ivec(jj)+1,:);

Ibb=find(~isnan(XwwLR));
Ibz=find(~isnan(XwwFQ));


NFFT=1024.*2.*2.*2.*2;

hh=spectrum.welch('hamming',NFFT./(2));

%hh=spectrum.mtm(6);
wwLR=XwwLR(Ibb); %+i.*YwwLR(Ibb);
wwFQ=XwwFQ(Ibz); %+i.*YwwFQ(Ibz);

LRpsdx=psd(hh,wwLR,'Fs', 0.003333333333333,'spectrumtype','onesided','NFFT',NFFT,'conflevel',0.95);
FQpsdx=psd(hh,wwFQ,'Fs', 0.003333333333333,'spectrumtype','onesided','NFFT',NFFT,'conflevel',0.95);
LRff=LRpsdx.Frequencies;
FQff=FQpsdx.Frequencies;

wwLRy=YwwLR(Ibb); %+i.*YwwLR(Ibb);
wwFQy=YwwFQ(Ibz); %+i.*YwwFQ(Ibz);

LRpsdy=psd(hh,wwLRy,'Fs', 0.003333333333333,'spectrumtype','onesided','NFFT',NFFT,'conflevel',0.95);
FQpsdy=psd(hh,wwFQy,'Fs', 0.003333333333333,'spectrumtype','onesided','NFFT',NFFT,'conflevel',0.95);


IxoLR=find(LRff>=3e-4 & LRff<=1e-3); %designating averaging areas..
IxoFQ=find(FQff>=3e-4 & FQff<=1e-3);

FQxavg(jj)=nanmean(FQpsdx.data(IxoFQ));
FQyavg(jj)=nanmean(FQpsdy.data(IxoFQ));
LRxavg(jj)=nanmean(LRpsdx.data(IxoLR));
LRyavg(jj)=nanmean(LRpsdy.data(IxoLR));



end

    fz1=figure;
%set(gca,'position',[.1 .1 0.9 0.9]);
set(fz1,'paperorientation','portrait','paperposition',[0.2500    0.2500   8 10.5000]);


subplot(2,2,1);
plot(FQxavg,Vel.z_adcp(Ivec),'r');
hold on
plot(LRxavg,-Vel.z_adcp(Ivec),'b.');
legend('FQ \Phi_u','RD \Phi_u','location','northeast');
set(gca,'xtick',[0:1:10],'xlim',[0 5]);
ylabel('dist. below xducer / m');
xlabel('spectral level / \Phi_{vel} m^2 s^{-1} Hz^{-1}');
axis ij

subplot(2,2,2);
plot(FQyavg,-Vel.z_adcp(Ivec),'r');
hold on
plot(LRyavg,-Vel.z_adcp(Ivec),'b.');
set(gca,'xtick',[0:1:10],'xlim',[0 5]);
axis ij

legend('FQ \Phi_v','RD \Phi_v','location','northeast');

subplot(2,2,3);
plot(sqrt(FQxavg./LRxavg),-Vel.z_adcp(Ivec),'r');
set(gca,'xtick',[0:1:6],'xlim',[0 4]);
grid on
legend('(FQ \Phi_{u, nl}/RD \Phi_{u,nl})^{1/2}','location','southeast');
axis ij

subplot(2,2,4);
plot(sqrt(FQyavg./LRyavg),-Vel.z_adcp(Ivec),'r');
set(gca,'xtick',[0:1:6],'xlim',[0 4]);
ylabel('dist. below xducer / m');
axis ij

grid on
legend('(FQ \Phi_{v, nl}/RD \Phi_{v,nl})^{1/2}','location','southeast');

% 
% pgdRD=nanmean([nanmean(Vel.pg1')' nanmean(Vel.pg1')' nanmean(Vel.pg1')' nanmean(Vel.pg1')']')';  
% pgdFQ=([nanmean(FQ.pgd.data')']./10).*100;  %this in percentage.. 
% 
% subplot(4,2,5);
% plot(pgdFQ,FQ.z,'r');
% hold on
% plot(pgdRD,Vel.z_adcp,'b.');
% 
% %set(gca,'xtick',[0:1:6],'xlim',[0 6]);
% grid on
% legend('(FQ y/RD y)^{1/2}','location','southeast');








% 
% 
% 
% 
% %smoothing in log-space
% Bb=boxcar(10)./nansum(boxcar(10));
% 
% FQpsdxI=interp1(log10(FQff(2:end)),FQpsd.data(2:end),[log10(FQff(2)):0.01:log10(FQff(end))]);
% FQpsdyI=interp1(log10(FQff(2:end)),FQpsdy.data(2:end),[log10(FQff(2)):0.01:log10(FQff(end))]);
% LRpsdxI=interp1(log10(LRff(2:end)),LRpsd.data(2:end),[log10(LRff(2)):0.01:log10(LRff(end))]);
% LRpsdyI=interp1(log10(LRff(2:end)),LRpsdy.data(2:end),[log10(LRff(2)):0.01:log10(LRff(end))]);
% 
% 
% 
% FQpsdSmx=conv2(1,Bb,FQpsdxI,'same');
% LRpsdSmx=conv2(1,Bb,LRpsdxI,'same');
% FQpsdSmy=conv2(1,Bb,FQpsdyI,'same');
% LRpsdSmy=conv2(1,Bb,LRpsdyI,'same');
% 
% FQfn=10.^[log10(FQff(2)):0.01:log10(FQff(end))];
% LRfn=10.^[log10(LRff(2)):0.01:log10(LRff(end))];
% 
% 
% subplot(5,2,jj.*2-1);
% loglog(FQfn,FQpsdSmx,'r-');
% hold on
% loglog(LRfn,LRpsdSmx,'b.');
% grid on
% set(gca,'xlim',[1e-4 2e-3],'ylim',[1e-1 1e1],'ytick',10.^[-1:1:2]);
% legend('FQ u','RDI u','location','northwest');
% 
% text(1.2e-4,2e-1,[num2str(round(-Vel.z_adcp(Ivec(jj)))) 'm']); 
% 
% ylabel('\Phi_{vel} m^2 s^{-2} Hz^{-1}');
% xlabel('Hz');
% 
% subplot(5,2,jj.*2);
% loglog(FQfn,FQpsdSmy,'r-');
% grid on
% hold on
% loglog(LRfn,LRpsdSmy,'b.');
% set(gca,'xlim',[1e-4 2e-3],'ylim',[1e-1 1e1],'ytick',10.^[-1:1:2]);
% 
% legend('FQ v','RDI v','location','northwest');
% 
% end













