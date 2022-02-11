% make a velocity structure for the M1 mooring

clear
mainpath = '/Users/awaterhouse/Documents/GitHub/niskine-proc/';
starttime = datenum(2019,5,13,0,0,0);
endtime = datenum(2020,10,20,0,0,0);
dt = 60; % in minutes, filtering time
dz = 16;

if 0
    % |  SN |Mooring|Performance|
    % |-----|-------|-----------|
    % | 3109|M1     |Full record|
    % | 9408|M1     |Full record|
    % |13481|M1     |Full record; issues with pressure time series|
    % |14408|M1     |Few days only|
    % |22476|M1     |Few days only|
    % | 3110|M2     |Full record|
    % | 8063|M2     |No data|
    % | 8065|M2     |Few days only; no pressure|
    % |10219|M2     |Full record|
    % |22479|M2     |Few days only|
    % |23615|M2     |Few days only|
    % |  344|M3     |No data|
    % | 8122|M3     |Few days only; no pressure|
    % |12733|M3     |Few days only|
    % |15339|M3     |Few days only|
    % |15694|M3     |Full record|
    %
    % Still need to work out a couple issues.
    %
    % **SN13481** has a full record, however, the pressure time series is not
    % realistic. It does show variations as the nearby pressure time series from
    % other ADCPs but I need to scale it by a factor of about 25 to get to realistic
    % pressure values. We are still in communication with RDI trying to figure out
    % what is going on here.
    %
    % **SN8065** and **SN8122** did not have pressure sensors. The processing code
    % still needs to be extended to allow for depth gridding. Since both instruments
    % returned only a few days of data, this has not been higher up on the priority list.
    
    m1path = '/Volumes/Ahua/data_archive/WaveChasers-DataArchive/NISKINE/Moorings/NISKINE19/M1/';
    m2path = '/Volumes/Ahua/data_archive/WaveChasers-DataArchive/NISKINE/Moorings/NISKINE19/M2/';
    m3path = '/Volumes/Ahua/data_archive/WaveChasers-DataArchive/NISKINE/Moorings/NISKINE19/M3/';
    
    
    for moor =1:3
        eval(['adcpfiles = dir([m' num2str(moor) 'path ''ADCP/proc/SN*'']);']);
        for i=1:length(adcpfiles)
            eval(['fnm = [m' num2str(moor) 'path ''ADCP/proc/'' adcpfiles(i).name ''/M' num2str(moor) '_'' adcpfiles(i).name(3:end) ''.nc''];']);
            if exist(fnm,'file')
                disp(['... reading M' num2str(moor) '_' adcpfiles(i).name(3:end) '.nc']);
                attdate = ncreadatt(fnm,'time','units');
                startdate = datenum(attdate(20:end));
                microtime = double(ncread(fnm,'time')); % time in microseconds
                eval(['adcp_' num2str(i) '.mtime = startdate + datenum(0,0,0,0,0,microtime/1e6);']);
                eval(['adcp_' num2str(i) '.z = ncread(fnm,''z'');']);
                eval(['adcp_' num2str(i) '.u = ncread(fnm,''u'');']);
                eval(['adcp_' num2str(i) '.v = ncread(fnm,''v'');']);
                eval(['adcp_' num2str(i) '.temperature = ncread(fnm,''temperature'');']);
                eval(['adcp_' num2str(i) '.pressure = ncread(fnm,''pressure'');']);
                
                eval(['m' num2str(moor) '_grid' num2str(i) '.mtime = starttime : datenum(0,0,0,0,dt,0): endtime;']);
                eval(['m' num2str(moor) '_grid' num2str(i) '.z = 0:dz:3000;']);
                
                eval(['m' num2str(moor) '_grid' num2str(i) '.u = interp2(adcp_' num2str(i) '.mtime'',adcp_' num2str(i) '.z,adcp_' num2str(i) '.u'',m' num2str(moor) '_grid' num2str(i) '.mtime,m' num2str(moor) '_grid' num2str(i) '.z'');']);
                eval(['m' num2str(moor) '_grid' num2str(i) '.v = interp2(adcp_' num2str(i) '.mtime'',adcp_' num2str(i) '.z,adcp_' num2str(i) '.v'',m' num2str(moor) '_grid' num2str(i) '.mtime,m' num2str(moor) '_grid' num2str(i) '.z'');']);
                eval(['m' num2str(moor) '_grid' num2str(i) '.p = interp1(adcp_' num2str(i) '.mtime'',adcp_' num2str(i) '.pressure,m' num2str(moor) '_grid' num2str(i) '.mtime);']);
                eval(['m' num2str(moor) '_grid' num2str(i) '.t = interp1(adcp_' num2str(i) '.mtime'',adcp_' num2str(i) '.temperature,m' num2str(moor) '_grid' num2str(i) '.mtime);']);
            end
        end
        clear adcp_*
    end
    
    % add flowquest mooring @ M2
    fqpath='/Users/awaterhouse/Documents/GitHub/niskine-proc/fq/fq_converted/';
    load([fqpath 'FQ_InterpolatedFinal.mat']);
    
    FQadcp.dnum = FQadcp.dnum(:,15:end);
    FQadcp.u = FQadcp.u(:,15:end);
    FQadcp.v = FQadcp.v(:,15:end);
    FQadcp.w = FQadcp.w(:,15:end);
    FQadcp.z = FQadcp.z(:,15:end);
    
    moor=2;
    i = 5;
    
    m2_grid5.mtime = starttime : datenum(0,0,0,0,dt,0): endtime;
    m2_grid5.z = 0:dz:3000;
    
    ufq = NaN(length(0:dz:3000),length(FQadcp.dnum));
    vfq = NaN(length(0:dz:3000),length(FQadcp.dnum));
    
    for j=1:length(FQadcp.dnum)
        ufq(:,j) = interp1(FQadcp.z(:,j),FQadcp.u(:,j), 0:dz:3000);
        vfq(:,j) = interp1(FQadcp.z(:,j),FQadcp.v(:,j), 0:dz:3000);
    end
    
    for k=1:size(ufq,1)
        m2_grid5.u(k,:) = interp1(FQadcp.dnum(1,:),ufq(k,:), starttime : datenum(0,0,0,0,dt,0): endtime);
        m2_grid5.v(k,:) = interp1(FQadcp.dnum(1,:),vfq(k,:), starttime : datenum(0,0,0,0,dt,0): endtime);
    end
    
    %%
    % M1:
    % 59� 6.087' N, 21� 11.930' W
    % Depth: 2881m
    
    % M2
    % 58� 57.959N, 21� 11.799W
    % Depth: 2894m
    
    % M3
    % 59� 1.813N, 21� 25.043W
    % Depth: 2900m
    
    for moor = 1:3
        eval(['clear M' num2str(moor)]);
        eval(['M' num2str(moor) '.mtime = m1_grid1.mtime;']);
        eval(['M' num2str(moor) '.z = m1_grid1.z;']);
        if moor ==1
            M1.lat = 59+6.087/60;
            M1.lon = 21+11.930/60;
            M1.maxd = 2881;
            M1.u = nanmedian(cat(3,m1_grid1.u,m1_grid2.u,m1_grid3.u,m1_grid4.u,m1_grid5.u),3);
            M1.u(M1.u==0)=NaN;
            M1.v = nanmedian(cat(3,m1_grid1.v,m1_grid2.v,m1_grid3.v,m1_grid4.v,m1_grid5.v),3);
            M1.v(M1.v==0)=NaN;
        elseif moor ==2
            M2.lat = 58+57.959/60;
            M2.lon = 21+11.799/60;
            M2.maxd = 2894;
            M2.u = nanmedian(cat(3,m2_grid1.u,m2_grid2.u,m2_grid3.u,m2_grid4.u,m2_grid5.u),3);
            M2.u(M2.u==0)=NaN;
            M2.v = nanmedian(cat(3,m2_grid1.v,m2_grid2.v,m2_grid3.v,m2_grid4.v,m2_grid5.v),3);
            M2.v(M2.v==0)=NaN;
        elseif moor ==3
            M3.lat = 59+1.813/60;
            M3.lon = 21+25.043/60;
            M3.maxd = 2900;
            M3.u = nanmedian(cat(3,m3_grid1.u,m3_grid2.u,m3_grid3.u),3);
            M3.u(M3.u==0)=NaN;
            M3.v = nanmedian(cat(3,m3_grid1.v,m3_grid2.v,m3_grid3.v),3);
            M3.v(M3.v==0)=NaN;
        end
        
        eval(['M' num2str(moor) '.u = interp_missing_data(M' num2str(moor) '.u);']);
        eval(['M' num2str(moor) '.v = interp_missing_data(M' num2str(moor) '.v);']);
        
        %[filtdat]=fourfilt(x,delt,tmax,tmin)
        %     where:   x:      data series to be filtered
        %              delt:   sampling interval
        %              tmax:   maximum period filter cutoff
        %              tmin:   minimum period filter cutoff
        
        eval(['Tni = 1./sw_f(M' num2str(moor) '.lat) * 1/60 * 1/60 * 2*pi; %~14 hrs']);
        
        eval(['M' num2str(moor) '.uf = NaN(size(M1.u));']);
        eval(['M' num2str(moor) '.vf = NaN(size(M1.v));']);
        eval(['szu = size(M' num2str(moor) '.u,1); ']);
        eval(['szt = size(M' num2str(moor) '.u,2); ']);
        
        %%% hmm, this bandpass code below is not quite right because I'm
        %%% bandpassing over data that has nan's removed (and chunks taken out
        %%% in time) and then piecing it back together, still need to fix this!
        
        testplot=0;
        for a=1:szu
            eval(['Mu = interp_missing_data(M' num2str(moor) '.u(a,:),5);'])
            eval(['Mv = interp_missing_data(M' num2str(moor) '.v(a,:),5);'])
            Mubp = NaN(size(Mu));
            Mvbp = NaN(size(Mv));
            
            if sum(~isnan(Mu))
                
                [idx_nan] =isnan(Mu);
                ii = find(idx_nan); % points that are nan
                bb=find(diff(ii)>1);
                indx_data = ii(bb); % indeces that have data in them...
                
                idx_notnan = ~isnan(Mu);
                jj = find(idx_notnan);
                cc=find(diff(jj)>1);
                indx_enddata = jj(cc);
                
                startingpoint = jj(1);
                endpoint = jj(end);
                
                if testplot
                    figure;
                    plot(M1.mtime,M1.u(a,:));
                    hold on;
                end
                for r=1:length(indx_data)
                    clear Mu_chunk_bp Mv_chunk_bp;
                    if r<length(indx_data)
                        Mu_chunk = Mu(indx_data(r)+1:indx_enddata(r));
                        Mv_chunk = Mv(indx_data(r)+1:indx_enddata(r));
                    else
                        Mu_chunk = Mu(indx_data(r)+1:endpoint);
                        Mv_chunk = Mv(indx_data(r)+1:endpoint);
                        
                    end
                    
                    if ~isempty(Mu_chunk) || length(Mu_chunk) > 300
                        if testplot
                            if r<length(indx_data)
                                plot(M1.mtime(indx_data(r)+1:indx_enddata(r)),Mu_chunk,'rx');
                            else
                                plot(M1.mtime(indx_data(r)+1:endpoint),Mu_chunk,'rx');
                            end
                            pause(0.1);
                        end
                        Mu_chunk_bp = fourfilt(demean(Mu_chunk),1,Tni+.1*Tni,Tni-.1*Tni);
                        Mv_chunk_bp = fourfilt(demean(Mv_chunk),1,Tni+.1*Tni,Tni-.1*Tni);
                        if r<length(indx_data)
                            Mubp(indx_data(r)+1:indx_enddata(r)) = Mu_chunk_bp;
                            Mvbp(indx_data(r)+1:indx_enddata(r)) = Mv_chunk_bp;
                        else
                            Mubp(indx_data(r)+1:endpoint) = Mu_chunk_bp;
                            Mvbp(indx_data(r)+1:endpoint) = Mv_chunk_bp;
                        end
                        if testplot
                            plot(M1.mtime,Mubp,'ok');
                            pause(0.1);
                        end
                    end
                end
            end
            
            eval(['M' num2str(moor) '.uf(a,:) = Mubp;']);
            eval(['M' num2str(moor) '.vf(a,:) = Mvbp;']);
        end
        %         eval(['[uu,jj,kk] = denan(M' num2str(moor) '.u(a,:)'');']);
        %         eval(['[vv,mm,nn] = denan(M' num2str(moor) '.v(a,:)'');']);
        %         if ~isempty(kk) && length(jj)<1000 %% the 1000 here is the thing that tells the bandpass to not go ahead if missing too much data
        %             eval(['M' num2str(moor) '.uf(a,kk) = fourfilt(demean(uu),1,Tni+.1*Tni,Tni-.1*Tni);']);
        %             eval(['M' num2str(moor) '.vf(a,nn) = fourfilt(demean(vv),1,Tni+.1*Tni,Tni-.1*Tni);']);
        %         end
        %end
        
        eval(['M' num2str(moor) '.uf_z = interp2(M' num2str(moor) '.mtime,M' num2str(moor) '.z(1:end-1)''+nanmean(diff(M' num2str(moor) '.z)),diff(M' num2str(moor) '.uf)./(nanmean(diff(M' num2str(moor) '.z))),M' num2str(moor) '.mtime,M1.z''); ']);
        eval(['M' num2str(moor) '.vf_z = interp2(M' num2str(moor) '.mtime,M' num2str(moor) '.z(1:end-1)''+nanmean(diff(M' num2str(moor) '.z)),diff(M' num2str(moor) '.vf)./(nanmean(diff(M' num2str(moor) '.z))),M' num2str(moor) '.mtime,M1.z''); ']);
        
        
        eval(['save ../M' num2str(moor) '.mat M' num2str(moor)]);
        
    end
end
clear m*_grid*
