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
# # NISKINe SBE37 data processing

# %% [markdown]
# ## Imports

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


# %% [markdown]
# ## Set paths

# %%
NISKINe_data = Path('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/')


# %% [markdown]
# Generate data paths depending on mooring / instrument serial number.

# %%
def construct_37_paths(sn, mooring):
    data_raw = NISKINe_data.joinpath(mooring).joinpath('SBE37/raw/SN{}'.format(sn))
    raw_file = list(data_raw.glob('*.cnv'))[0]
    data_out = NISKINe_data.joinpath(mooring).joinpath('SBE37/proc/SN{}'.format(sn))
    if not data_out.exists():
        data_out.mkdir()
    fig_out = NISKINe_data.joinpath(mooring).joinpath('SBE37/fig/')
    if not fig_out.exists():
        fig_out.mkdir()
    return data_raw, raw_file, data_out, fig_out


# %% [markdown]
# ## Read time offsets

# %%
offset_file = NISKINe_data.joinpath('SBE37_time_offsets.txt')

# %%
time_offsets = pd.read_csv(offset_file, engine='python', header=0, delim_whitespace=True, parse_dates={'utc': [3, 4], 'inst': [1, 2]}, index_col='SN')

# %%
time_offsets

# %% [markdown]
# ## Read newer instruments

# %% [markdown]
# The batteries on these instruments did not last as expected, records drop out in early 2020.

# %% [markdown]
# Visual comparison with a working microcat (SN2864) on the same mooring shows these times for last good data points on each microcat:
#
# 12710: 2020-02-09 21:00
#
# 12711: 2020-03-17 12:00
#
# 12712: 2020-01-16 23:15 

# %% [markdown]
# ### 12710

# %%
data_raw, raw_file, data_out, fig_out = construct_37_paths(12710, 'M1')
insttime = time_offsets.loc[12710].inst.to_datetime64()
utctime = time_offsets.loc[12710].utc.to_datetime64()
cuttime = gv.time.str_to_datetime64('2020-02-09 21:00')

# %%
sn12710 = sbe.sbe37.proc(raw_file, insttime, utctime, data_out=data_out, figure_out=fig_out, cut_time=cuttime)

# %% [markdown]
# ### 12711

# %%
data_raw, raw_file, data_out, fig_out = construct_37_paths(12711, 'M1')
insttime = time_offsets.loc[12711].inst.to_datetime64()
utctime = time_offsets.loc[12711].utc.to_datetime64()
cuttime = gv.time.str_to_datetime64('2020-03-17 12:00')

# %%
sn12711 = sbe.sbe37.proc(raw_file, insttime, utctime, data_out=data_out, figure_out=fig_out, cut_time=cuttime)

# %% [markdown]
# ### 12712

# %%
data_raw, raw_file, data_out, fig_out = construct_37_paths(12712, 'M1')
insttime = time_offsets.loc[12712].inst.to_datetime64()
utctime = time_offsets.loc[12712].utc.to_datetime64()
cuttime = gv.time.str_to_datetime64('2020-01-16 23:15')

# %%
sn12712 = sbe.sbe37.proc(raw_file, insttime, utctime, data_out=data_out, figure_out=fig_out, cut_time=cuttime)

# %% [markdown]
# Anomalous event on M1 in pressure Oct 7 around 20:00. 

# %%
timeslice=slice('2019-10-5', '2019-10-10')
fig, ax = gv.plot.quickfig()
sn12710.p.sel(time=timeslice).plot()
sn12711.p.sel(time=timeslice).plot();

# %% [markdown]
# ## Read old instruments

# %% [markdown]
# The older SBE37s don't come with time stamps and variable names are slightly different.
#
# These all seem to have worked as expected.

# %% [markdown]
# ### 2864

# %%
data_raw, raw_file, data_out, fig_out = construct_37_paths(2864, 'M1')
insttime = time_offsets.loc[2864].inst.to_datetime64()
utctime = time_offsets.loc[2864].utc.to_datetime64()

# %%
sn2864 = sbe.sbe37.proc(raw_file, insttime, utctime, data_out=data_out, figure_out=fig_out)

# %% [markdown]
# ### 3638

# %%
data_raw, raw_file, data_out, fig_out = construct_37_paths(3638, 'M3')
insttime = time_offsets.loc[3638].inst.to_datetime64()
utctime = time_offsets.loc[3638].utc.to_datetime64()

# %%
sn3638 = sbe.sbe37.proc(raw_file, insttime, utctime, data_out=data_out, figure_out=fig_out)

# %% [markdown]
# ### 4922

# %%
data_raw, raw_file, data_out, fig_out = construct_37_paths(4922, 'M2')
insttime = time_offsets.loc[4922].inst.to_datetime64()
utctime = time_offsets.loc[4922].utc.to_datetime64()

# %%
sn4922 = sbe.sbe37.proc(raw_file, insttime, utctime, data_out=data_out, figure_out=fig_out)

# %% [markdown]
# ### 4923

# %%
data_raw, raw_file, data_out, fig_out = construct_37_paths(4923, 'M1')
insttime = time_offsets.loc[4923].inst.to_datetime64()
utctime = time_offsets.loc[4923].utc.to_datetime64()

# %%
sn4923 = sbe.sbe37.proc(raw_file, insttime, utctime, data_out=data_out, figure_out=fig_out)

# %%
