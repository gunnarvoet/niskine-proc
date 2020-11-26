# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # NISKINe SBE56 data processing

# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
from pathlib import Path

import gvpy as gv
import sbemoored as sbe

# %reload_ext autoreload
# %autoreload 2
# %autosave 300

plt.ion()

# %config InlineBackend.figure_format = 'retina'


# %%
# set to true to run exploratory code snippets below
dev = False

# %% [markdown]
# ## Set paths

# %%
NISKINe_data = Path('/Users/gunnar/Projects/niskine/data/')

# %%
sbe56_data = NISKINe_data.joinpath('Moorings/NISKINE19/M1/SBE56')

# %%
raw_data = sbe56_data.joinpath('raw/csv')

# %%
data_out = sbe56_data.joinpath('proc')

# %%
fig_out = sbe56_data.joinpath('fig')
if not fig_out.exists():
    fig_out.mkdir()

# %% [markdown]
# ## Read time offsets

# %%
offset_file = sbe56_data.joinpath('SBE56_time_offsets.txt')

# %%
time_offsets = pd.read_csv(offset_file, engine='python', header=0, delim_whitespace=True, parse_dates={'utc': [3, 4], 'inst': [1, 2]}, index_col='SN')

# %%
time_offsets

# %% [markdown]
# ## Process example file

# %%
if dev:
    sn = 395
    utctime = time_offsets.loc[sn]['utc'].to_datetime64()
    insttime = time_offsets.loc[sn]['inst'].to_datetime64()

    testfile = list(raw_data.glob('SBE056{:05d}*.csv'.format(sn)))
    testfile = testfile[0]

    t = sbe.sbe56.proc(testfile, time_instrument=insttime, time_utc=utctime, data_out=data_out, figure_out=fig_out, show_plot=True)

# %% [markdown]
# ## Process all

# %%
for sn, times in time_offsets.iterrows():
    utctime = times.utc.to_datetime64()
    insttime = times.inst.to_datetime64()
    print(sn)
    file = list(raw_data.glob("SBE056{:05d}*.csv".format(sn)))
    file = file[0]
    t = sbe.sbe56.proc(
        file,
        time_instrument=insttime,
        time_utc=utctime,
        data_out=data_out,
        figure_out=fig_out,
        show_plot=True,
    )
    

# %% [markdown]
# ## Investigate gaps

# %%
if dev:
    tmp = xr.open_dataarray('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/SBE56/proc/SBE05606435_2020-10-07.nc')

    fig, ax = gv.plot.quickfig()
    tmp.plot(marker='.', linestyle='')

# %% [markdown]
# Looks like there is simply data missing. How could this have happened? Maybe bad downloads?

# %% [markdown]
# ## Plot ends of time series

# %% [markdown]
# load all files and select Oct 2020

# %%
if dev:
    timesel = slice('2020-09', '2020-11')

    all_files = list(sorted(data_out.glob('*.nc')))
    aa = []
    for f in all_files:
        aa.append(xr.open_dataarray(f).sel(time=timesel))

    pdtime = pd.period_range(start=np.datetime64('2020-09-01'), end=np.datetime64('2020-10-12'), freq='2min')
    new_time = pdtime.to_timestamp()
    new_time = new_time.to_numpy()

    ab = []
    for ai in aa:
        try:
            tmp = ai.interp({'time': new_time})
            ab.append(tmp)
        except:
            ai

    a = xr.concat(ab, dim='n')

    fig, ax = gv.plot.quickfig()
    a.plot(hue='n', add_legend=False);

# %% [markdown]
# ## Plot all time series

# %% [markdown]
# load all files

# %%
if dev:
    all_files = list(sorted(data_out.glob('*.nc')))
    aa = []
    for f in all_files:
        aa.append(xr.open_dataarray(f))

    # ten-minute averages, interpolate to common time vector
    pdtime = pd.period_range(start=np.datetime64('2019-05-10'), end=np.datetime64('2020-10-06'), freq='10min')
    new_time = pdtime.to_timestamp()
    new_time = new_time.to_numpy()

    ab = []
    for ai in aa:
        tr = ai.rolling(time=60).mean()
        ab.append(tr.interp({'time': new_time}))

    a = xr.concat(ab, dim='n')

    fig, ax = gv.plot.quickfig(fgs=(8, 6))
    a.plot(hue='n', add_legend=False, ax=ax);

# %%
