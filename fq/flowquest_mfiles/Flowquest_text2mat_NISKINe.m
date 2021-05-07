%This script processes Flowquest text data files created by
%"Conversion Tool A"


%set parameters below:


 Instdepth=0;  %set to zero if you want z to be relative to the transducer
 BinLength=16;
%Declin=10.6 % %10.6 for SAMOA...positive east, negative west (CDMVTAE! or TVMDCAW!)
Declin=-10.9; %for NISKINe 2019/2020

%path='/volumes/Puao/data_archive/WaveChasers-DataArchive/SamoanPassage/Moorings/sp12/P1/Flowquest/rawdata/';

path='/Users/johnmickett/Cruises_Research/NISKINe/fq_converted/';

%path='/Users/johnmickett/Cruises_Research/SPAM_EX/flowquest/flowquest_M6n/'


%cd /Users/johnmickett/Cruises_Research/MC09/Flowquest/mendo09offload1/

cd /Users/johnmickett/Cruises_Research/NISKINe/fq_converted/;

%cd /Users/johnmickett/Cruises_Research/SPAM_EX/flowquest/flowquest_M6n/
%cd /volumes/Puao/data_archive/WaveChasers-DataArchive/SamoanPassage/Moorings/sp12/P1/Flowquest/rawdata/;


DdM=dir;


%getting DAT file names...
jj=1;
for ii=1:length(DdM);
    fname=DdM(ii).name;
    if length(fname)==15;
        Idf=strmatch('DAT.txt',fname(:,9:15)); %these are text files
        if ~isempty(Idf);
            VecID(jj)=ii;
            jj=jj+1;
        end
    end
end


%below was changed to just edit the 2007 data!
%Idf=find(DdM(:,9)=='V' & DdM(:,6)=='5');

DdM=DdM(VecID,:);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%sub-routine: we're getting an approximate file size to make blank
%matrices
plen=0;
NumBinVel=0;
ENS_L=0;


for jd=1:length(DdM);

    fid=fopen([path DdM(jd).name]);

    %jd


    while 1
        LGETT=fgets(fid);

        if LGETT==-1;
            %disp('parsing complete');
            break
        end

        if strcmp(LGETT(1:2),'E3')==1;

            OUTT_Ea=strread(LGETT,'%s');
            NumBinVela=str2num(OUTT_Ea{2})./3;
            if NumBinVela~=0;
                plen=plen+1;

            end
            if NumBinVela>NumBinVel;
                NumBinVel=NumBinVela;
            end

        end

        if strcmp(LGETT(1:2),'E1')==1;

            OUTT_Eaa=strread(LGETT,'%s');
            ENS_La=str2num(OUTT_Eaa{2})./3;
            if ENS_La>ENS_L;
                ENS_L=ENS_La;
            end

        end


    end
    fclose(fid);

end


%creating matrices of NaNs based on "NumBinVel" and "plen" and ensemble
%length (ENS_L)

INIT_mat=NaN.*ones(NumBinVel,plen);  %initialization matrix
INIT_vec=NaN.*ones(1,plen);  %initialization vector
INIT_ens=NaN.*ones(ENS_L,plen);



FQ.ensNO=INIT_vec;
%01-Mar-2000 15:45:17
FQ.DateNum=INIT_vec;
FQ.yday =INIT_vec;
FQ.Engr.Temp=INIT_vec;
FQ.Engr.Voltage=INIT_vec;
FQ.NumPings=INIT_vec;
FQ.BinLength=INIT_vec;
FQ.xDucerDepth=INIT_vec;
FQ.Engr.BlankDist=INIT_vec;
FQ.Engr.Err=INIT_vec;
FQ.Engr.AbNoRPH=INIT_vec;

FQ.roll_mean=INIT_vec;
FQ.roll_std=INIT_vec;
FQ.pitch_mean=INIT_vec;
FQ.pitch_std=INIT_vec;
FQ.head_mean=INIT_vec;
FQ.head_std=INIT_vec;


%need ensemble size here

FQ.roll=INIT_ens;
FQ.pitch=INIT_ens;
FQ.head=INIT_ens;

FQ.RadVel.ch0=INIT_mat;
FQ.RadVel.ch1=INIT_mat;
FQ.RadVel.ch2=INIT_mat;
FQ.RadVel.ch3=INIT_mat;

FQ.InstVel.Vy=INIT_mat;
FQ.InstVel.Vx=INIT_mat;
FQ.InstVel.Vz=INIT_mat;

FQ.Vely=INIT_mat;
FQ.Velx=INIT_mat;
FQ.Velz=INIT_mat;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%IMPT, make sure binlength is correct below (16 m, 8m, etc.)
NumBins=INIT_vec;

%percent good
FQ.pgd.data=INIT_mat; %Vx

%signal strength
FQ.SigStr.ch0=INIT_mat;
FQ.SigStr.ch1=INIT_mat;
FQ.SigStr.ch2=INIT_mat;
FQ.SigStr.ch3=INIT_mat;

%signal to noise ratio
FQ.SNR.ch0=INIT_mat;
FQ.SNR.ch1=INIT_mat;
FQ.SNR.ch2=INIT_mat;
FQ.SNR.ch3=INIT_mat;


k=0; %counter to 1

fclose all;

for jp=1:length(DdM);

    jp

 fid=fopen([path DdM(jp).name]);

    %fid=fopen(['C:\Cruises_Research\PhilEx\fqshort.txt']);


    %    h = waitbar(0,'Please wait...');
    %         for i=1:1000,
    %             % computation here %
    %             waitbar(i/1000,h);
    %         end


    %while fgets(fid)~=-1; %will read until end of file indicator (-1).
    while 1
        LGETT=fgets(fid);

        if LGETT==-1;
            %disp('parsing complete');
            break
        end




        if strcmp(LGETT(1:2),'$#')==1;

            if mod(k,20)==0;
                fprintf('.');
                %sprintf('%s','.');
            end


        elseif ~isempty(findstr(LGETT,'0x1EF'))==1;  %this will recognize the header line with the date

            % %if we detect a header, we have an ensemble...
            %     k=1+k;


            %[Aa]=textscan(LGETT,'%s','delimiter',' ');
            %OUTT=Aa{1};

            OUTT_HDR=strread(LGETT,'%s');




            HHMMSS=OUTT_HDR{5};

            %getting yearday
            Mostr={'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'};
            Icc=strmatch(OUTT_HDR{3},Mostr);


        elseif strcmp(LGETT(1:2),'E0')==1; %parse ensemble mean roll, pitch, heading info

            OUTT_E0=strread(LGETT,'%s');

        elseif strcmp(LGETT(1:2),'E1')==1; %parse roll, pitch, heading info for each ping
            %this is dependent upon the number of pings per ensemble...so we need to
            %think carefully about this..


            OUTT_E1=strread(LGETT,'%s');
            NoVal=str2num(OUTT_E1{2});

            RPH=NaN.*ones(1,size(OUTT_E1,1)-2);
            for jj=3:size(OUTT_E1,1);
                RPH(jj-2)=str2num(OUTT_E1{jj});
            end
            RPHa=[RPH(1:3:end-2)' RPH(2:3:end-1)' RPH(3:3:end)'];


        elseif strcmp(LGETT(1:2),'E2')==1; %parse radial velocity data



            OUTT_E2=strread(LGETT,'%s');
            NumBin=str2num(OUTT_E2{2})./4;

            %if NumBin=0 this means that there is no good data--so we need
            %NaN's

            if NumBin~=0;

                RV=NaN.*ones(1,size(OUTT_E2,1)-2);
                for jj=3:size(OUTT_E2,1);
                    RV(jj-2)=str2num(OUTT_E2{jj});
                end

                RV2=reshape(RV,NumBin,4);

            end



        elseif strcmp(LGETT(1:2),'E3')==1; %parse instrument coordinate data

            OUTT_E3=strread(LGETT,'%s');
            NumBin=str2num(OUTT_E3{2})./3;


            if NumBin~=0;

                IVel=NaN.*ones(1,size(OUTT_E3,1)-2);
                for jj=3:size(OUTT_E3,1);
                    IVel(jj-2)=str2num(OUTT_E3{jj});
                end

                IV=[IVel(1:3:end-2)' IVel(2:3:end-1)' IVel(3:3:end)'];

            end

%% no earth coordinate data in NISKINE

%         elseif strcmp(LGETT(1:2),'E4')==1; %parse Earth coordinate data
%        
%      
% 
%             OUTT_E4=strread(LGETT,'%s');
%             NumBinVel=str2num(OUTT_E4{2})./3;
% 
% 
%             if NumBinVel~=0;
% 
%                 IVel=NaN.*ones(1,size(OUTT_E4,1)-2);
%                 for jj=3:size(OUTT_E4,1);
%                     IVel(jj-2)=str2num(OUTT_E4{jj});
%                 end
% 
%                 IV2=[IVel(1:3:end-2)' IVel(2:3:end-1)' IVel(3:3:end)'];
% 
% 
%             end



        elseif strcmp(LGETT(1:2),'E5')==1; %percentage good

            OUTT_E5=strread(LGETT,'%s');
            NumBin=str2num(OUTT_E5{2});


            if NumBin~=0;

                Pgdd=NaN.*ones(NumBin,1);
                for jj=3:size(OUTT_E5,1);
                    Pgdd(jj-2)=str2num(OUTT_E5{jj});
                end


            end



        elseif strcmp(LGETT(1:2),'E6')==1; %signal strength in dBm

            OUTT_E6=strread(LGETT,'%s');
            NumBin=str2num(OUTT_E6{2})./4;

            if NumBin~=0;

                SigStr=NaN.*ones(1,size(OUTT_E6,1)-2);
                for jj=3:size(OUTT_E6,1);
                    SigStr(jj-2)=str2num(OUTT_E6{jj});
                end

                SigStr=reshape(SigStr,NumBin,4);

            end


        elseif strcmp(LGETT(1:2),'E7')==1; %SNR in DB


            OUTT_E7=strread(LGETT,'%s');
            NumBin=str2num(OUTT_E7{2})./4;

            if NumBin~=0;

                SNR=NaN.*ones(1,size(OUTT_E7,1)-2);
                for jj=3:size(OUTT_E7,1);
                    SNR(jj-2)=str2num(OUTT_E7{jj});
                end

                SNR=reshape(SNR,NumBin,4);

            end

            
            
          elseif strcmp(LGETT(1:2),'E8')==1; %instrument pressure in bars * 4


             OUTT_E8=strread(LGETT,'%s');
               XDucerPres=str2num(OUTT_E8{2})./4./100;

     

            %if we have radial velocity measured, we have an ensemble...
            if exist('RV') & exist('IV');

                k=1+k;  %advancing counter

                FQ.ensNO(k)=str2num(OUTT_HDR{1});
                %01-Mar-2000 15:45:17
                FQ.DateNum(k)=datenum([OUTT_HDR{4} '-' OUTT_HDR{3} '-' OUTT_HDR{6} ' ' OUTT_HDR{5}],0);
                FQ.yday(k)=yearday(str2num(OUTT_HDR{4}),Icc,str2num(OUTT_HDR{6}),str2num(HHMMSS(1:2)),str2num(HHMMSS(4:5)),str2num(HHMMSS(7:8)));
                FQ.Date{k}=[OUTT_HDR{4} '-' OUTT_HDR{3} '-' OUTT_HDR{6} ' ' OUTT_HDR{5}];
                FQ.Engr.Temp(k)=str2num(OUTT_HDR{7});
                FQ.Engr.Voltage(k)=str2num(OUTT_HDR{8});
                FQ.NumPings(k)=str2num(OUTT_HDR{9});
                FQ.BinLength(k)=str2num(OUTT_HDR{20})./100; %in meters
                FQ.xDucerNomDepth(k)=str2num(OUTT_HDR{29});
                FQ.Engr.BlankDist(k)=str2num(OUTT_HDR{30})./100;
                FQ.Engr.Err(k)=str2num(OUTT_HDR{31});  %error code, 0 no-error, non-zero indicates error
                FQ.Engr.AbNoRPH(k)=str2num(OUTT_HDR{32}); %number of pings with abnormal roll pitch and heading which are discarded
                FQ.xDucerPresDBar(k)=XDucerPres;

                FQ.roll_mean(k)=str2num(OUTT_E0{3});
                FQ.roll_std(k)=str2num(OUTT_E0{4});
                FQ.pitch_mean(k)=str2num(OUTT_E0{5});
                FQ.pitch_std(k)=str2num(OUTT_E0{6});
                FQ.head_mean(k)=str2num(OUTT_E0{7});
                FQ.head_std(k)=str2num(OUTT_E0{8});

                FQ.roll(1:size(RPHa,1),k)=RPHa(:,1);
                FQ.pitch(1:size(RPHa,1),k)=RPHa(:,2);
                FQ.head(1:size(RPHa,1),k)=RPHa(:,3);


                FQ.RadVel.ch0(1:size(RV2,1),k)=RV2(:,1)./1000;
                FQ.RadVel.ch1(1:size(RV2,1),k)=RV2(:,2)./1000;
                FQ.RadVel.ch2(1:size(RV2,1),k)=RV2(:,3)./1000;
                FQ.RadVel.ch3(1:size(RV2,1),k)=RV2(:,4)./1000;




                FQ.InstVel.Vy(1:size(IV,1),k)=(IV(:,1)./1000); %Vx
                FQ.InstVel.Vx(1:size(IV,1),k)=(IV(:,2)./1000); %Vx
                FQ.InstVel.Vz(1:size(IV,1),k)=(IV(:,3)./1000); %Vx



if exist('IV2','var');
                FQ.Vely(1:size(IV2,1),k)=(IV2(:,1)./1000); %Vy
                FQ.Velx(1:size(IV2,1),k)=(IV2(:,2)./1000); %Vx
                FQ.Velz(1:size(IV2,1),k)=(IV2(:,3)./1000); %Vw
% else
%      FQ.Vely(1:size(IV,1),k)=NaN.*(IV(:,1)./1000); %Vy
%                 FQ.Velx(1:size(IV,1),k)=NaN.*(IV(:,2)./1000); %Vx
%                 FQ.Velz(1:size(IV,1),k)=NaN.*(IV(:,3)./1000); %Vw
end

    

                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %IMPT, make sure binlength is correct below (16 m, 8m, etc.)
                NumBins(k)=NumBin;

               
                FQ.z=Instdepth+FQ.Engr.BlankDist(1)+BinLength./2+([0:1:(nanmax(NumBins)-1)].*BinLength);

                %percent good
                FQ.pgd.data(1:length(Pgdd),k)=Pgdd; %Vx

                %signal strength
                FQ.SigStr.ch0(1:size(SigStr,1),k)=SigStr(:,1);
                FQ.SigStr.ch1(1:size(SigStr,1),k)=SigStr(:,2);
                FQ.SigStr.ch2(1:size(SigStr,1),k)=SigStr(:,3);
                FQ.SigStr.ch3(1:size(SigStr,1),k)=SigStr(:,4);


                %signal to noise ratio
                FQ.SNR.ch0(1:size(SNR,1),k)=SNR(:,1);
                FQ.SNR.ch1(1:size(SNR,1),k)=SNR(:,2);
                FQ.SNR.ch2(1:size(SNR,1),k)=SNR(:,3);
                FQ.SNR.ch3(1:size(SNR,1),k)=SNR(:,4);




            end

            clear RV SNR SigStr Pgdd IV2 IV RV2 RPHa


        end


    end

end


%rotating u an v velocities to convert from mag. to true directions.
Uu=FQ.Velx;
Vv=FQ.Vely;

[Tha,Rha]=cart2pol(Uu,Vv);
FQdeg=rad2degT(Tha);
FQdegCor=FQdeg+Declin;
ThaCorr=degT2rad(FQdegCor);
[Uua,Vva]=pol2cart(ThaCorr,Rha);

FQ.Velx=Uua;
FQ.Vely=Vva;


FQ.Engr_readme{1}='BlankDist is blanking distance in meters';
FQ.Engr_readme{2}='Err is error code: 0 no-error, non-zero indicates number of pings with errors.';
FQ.Engr_readme{3}='AbNoRPH is number of pings with abnormal roll, pitch and head THAT ARE DISCARDED';
FQ.Engr_readme{4}='Bin length should be in meters, but there were some oddities in the data';
FQ.rph_info='roll, pitch, head are values for each ping of the ensemble';
FQ.RadVel.info='beam radial velocity for ch0,ch1,ch2,ch3 in m/s';
FQ.InstVel.info='x dir. is 3->1, y dir is 4->2, z is vertical following right hand rule. See manual.';
FQ.info='created with Flowquest_text2mat. Vels in m/s';
FQ.pgd.info='this is the NUMBER of good pings in ensemble, NOT percentage of pings good';
FQ.SigStr.info='Signal Strength in dBm';
FQ.SNR.info='Signal to noise ratio in dB';
FQ.declination=Declin;

