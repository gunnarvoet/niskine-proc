# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
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
import sbe

# %reload_ext autoreload
# %autoreload 2
# %autosave 0

plt.ion()

# %config InlineBackend.figure_format = 'retina'


# %% [markdown]
# ## Set paths

# %%
data_out = Path('/Users/gunnar/Projects/niskin/data/moorings/proc/sbe56/')

# %%
fig_out = Path('/Users/gunnar/Projects/niskin/data/moorings/proc/sbe56/fig/')
if ~fig_out.exists():
    fig_out.mkdir()

# %% [markdown]
# ## Read time offsets

# %%
offset_file = 'SBE56_time_offsets.txt'

# %%
time_offsets = pd.read_csv(offset_file, engine='python', header=0, delim_whitespace=True, parse_dates={'utc': [3, 4], 'inst': [1, 2]}, index_col='SN')

# %%
time_offsets

# %% [markdown]
# ## Process example file

# %%
sn = 395
utctime = time_offsets.loc[sn]['utc'].to_datetime64()
insttime = time_offsets.loc[sn]['inst'].to_datetime64()

# %%
raw_data = Path('/Users/gunnar/Projects/niskin/data/moorings/raw/SBE56/csv/')

# %%
testfile = list(raw_data.glob('SBE056{:05d}*.csv'.format(sn)))
testfile = testfile[0]

# %%
t = sbe.sbe56.proc(testfile, time_instrument=insttime, time_utc=utctime, data_out=data_out, figure_out=fig_out, show_plot=True)

# %% [markdown]
# ## Process all

# %%
raw_data = Path('/Users/gunnar/Projects/niskin/data/moorings/raw/SBE56/csv/')

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

# %%

# %% [markdown]
# ## Plot all time series

# %% [markdown]
# load all files

# %%
all_files = list(sorted(data_out.glob('*.nc')))
aa = []
for f in all_files:
    aa.append(xr.open_dataarray(f))

# %% [markdown]
# ten-minute averages, interpolate to common time vector

# %%
pdtime = pd.period_range(start=np.datetime64('2019-05-10'), end=np.datetime64('2020-10-06'), freq='10min')
new_time = pdtime.to_timestamp()
new_time = new_time.to_numpy()

# %%
ab = []
for ai in aa:
    tr = ai.rolling(time=60).mean()
    ab.append(tr.interp({'time': new_time}))

# %%
a = xr.concat(ab, dim='n')

# %%
aa[0]

# %%
fig, ax = gv.plot.quickfig(fgs=(8, 6))
a.plot(hue='n', add_legend=False, ax=ax);

# %%
