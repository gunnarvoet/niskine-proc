%This script processes Flowquest text data files created by
%"Conversion Tool A"

path='C:\Cruises_Research\PhilEx\';

cd C:\Cruises_Research\PhilEx


k=0; %counter to 1



    fid=fopen([path 'FQ_Philex_test.txt']);

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


        elseif ~isempty(findstr(LGETT,'0xFF'))==1;  %this will recognize the header line with the date

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



        elseif strcmp(LGETT(1:2),'E4')==1; %parse Earth coordinate data

            OUTT_E4=strread(LGETT,'%s');
            NumBinVel=str2num(OUTT_E4{2})./3;


            if NumBinVel~=0;

                IVel=NaN.*ones(1,size(OUTT_E4,1)-2);
                for jj=3:size(OUTT_E4,1);
                    IVel(jj-2)=str2num(OUTT_E4{jj});
                end

                IV2=[IVel(1:3:end-2)' IVel(2:3:end-1)' IVel(3:3:end)'];
              

            end



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
            FQ.xDucerDepth(k)=str2num(OUTT_HDR{29});
            FQ.Engr.BlankDist(k)=str2num(OUTT_HDR{30})./100;
            FQ.Engr.Err(k)=str2num(OUTT_HDR{31});  %error code, 0 no-error, non-zero indicates error
            FQ.Engr.AbNoRPH(k)=str2num(OUTT_HDR{32}); %number of pings with abnormal roll pitch and heading which are discarded

            FQ.Engr_readme{1}='BlankDist is blanking distance in meters';
            FQ.Engr_readme{2}='Err is error code: 0 no-error, non-zero indicates number of pings with errors.';
            FQ.Engr_readme{3}='AbNoRPH is number of pings with abnormal roll, pitch and head THAT ARE DISCARDED';
            FQ.Engr_readme{4}='Bin length should be in meters, but there were some oddities in the data';

            FQ.roll_mean(k)=str2num(OUTT_E0{3});
            FQ.roll_std(k)=str2num(OUTT_E0{4});
            FQ.pitch_mean(k)=str2num(OUTT_E0{5});
            FQ.pitch_std(k)=str2num(OUTT_E0{6});
            FQ.head_mean(k)=str2num(OUTT_E0{7});
            FQ.head_std(k)=str2num(OUTT_E0{8});
                
            FQ.roll(1:size(RPHa,1),k)=RPHa(:,1);
            FQ.pitch(1:size(RPHa,1),k)=RPHa(:,2);
            FQ.head(1:size(RPHa,1),k)=RPHa(:,3);
            FQ.rph_info='roll, pitch, head are values for each ping of the ensemble';
                
                FQ.RadVel.ch0(1:size(RV2,1),k)=RV2(:,1)./1000;
                FQ.RadVel.ch1(1:size(RV2,1),k)=RV2(:,2)./1000;
                FQ.RadVel.ch2(1:size(RV2,1),k)=RV2(:,3)./1000;
                FQ.RadVel.ch3(1:size(RV2,1),k)=RV2(:,4)./1000;
                FQ.RadVel.info='beam radial velocity for ch0,ch1,ch2,ch3 in m/s';    
                
                FQ.InstVel.Vy(1:size(IV,1),k)=(IV(:,1)./1000); %Vx
                FQ.InstVel.Vx(1:size(IV,1),k)=(IV(:,2)./1000); %Vx
                FQ.InstVel.Vz(1:size(IV,1),k)=(IV(:,3)./1000); %Vx
                FQ.InstVel.info='x dir. is 3->1, y dir is 4->2, z is vertical following right hand rule. See manual.';

                FQ.Vely(1:size(IV2,1),k)=(IV2(:,1)./1000); %Vx
                FQ.Velx(1:size(IV2,1),k)=(IV2(:,2)./1000); %Vx
                FQ.Velz(1:size(IV2,1),k)=(IV2(:,3)./1000); %Vx
                FQ.info='created with Flowquest_text2mat. Vels in m/s';
                
                                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %IMPT, make sure binlength is correct below (16 m, 8m, etc.)
                 NumBins(k)=NumBinVel;
                
                Instdepth=30;
                BinLength=16;
                FQ.z=Instdepth+FQ.Engr.BlankDist(1)+BinLength./2+([0:1:(nanmax(NumBins)-1)].*BinLength);
                
                %percent good
                FQ.pgd.data(1:length(Pgdd),k)=Pgdd; %Vx
                FQ.pgd.info='this is the NUMBER of good pings in ensemble, NOT percentage of pings good';
                
                %signal strength
                FQ.SigStr.ch0(1:size(SigStr,1),k)=SigStr(:,1);
                FQ.SigStr.ch1(1:size(SigStr,1),k)=SigStr(:,2);
                FQ.SigStr.ch2(1:size(SigStr,1),k)=SigStr(:,3);
                FQ.SigStr.ch3(1:size(SigStr,1),k)=SigStr(:,4);

                FQ.SigStr.info='Signal Strength in dBm';
                
                %signal to noise ratio
                FQ.SNR.ch0(1:size(SNR,1),k)=SNR(:,1);
                FQ.SNR.ch1(1:size(SNR,1),k)=SNR(:,2);
                FQ.SNR.ch2(1:size(SNR,1),k)=SNR(:,3);
                FQ.SNR.ch3(1:size(SNR,1),k)=SNR(:,4);
                FQ.SNR.info='Signal to noise ratio in dB';
                
                
              
            end

            clear RV SNR SigStr Pgdd IV2 IV RV2 RPHa


        end


    end
