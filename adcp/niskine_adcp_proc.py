# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# #### Imports

# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
from pathlib import Path
import datetime

import gvpy as gv
import gadcp

# load local functions
import niskine_adcp_proc_functions as nap

# %reload_ext autoreload
# %autoreload 2
# %autosave 300

plt.ion()

# %config InlineBackend.figure_format = 'retina'


# %% [markdown]
# # NISKINe ADCP data processing

# %% [markdown]
# Project-specific processing functions are imported from the local `niskine_adcp_proc_functions`.
#
# The package `gadcp` wraps the UH `pycurrents` package which must be installed separately from the conda environment provided with this repository. An installation guide for the UH software can be found [here](https://currents.soest.hawaii.edu/ocn_data_analysis/installation.html). Make sure to install the UH software into the same conda environment as the rest of the packages from `environment.yml`.

# %% [markdown]
# ## Set parameters

# %% [markdown]
# Set the path to your local mooring data directory; this is the directory level that contains folders `M1`, `M2`, and `M3`, for individual moorings.

# %%
NISKINe_data = Path('/Users/gunnar/Projects/niskine/data/NISKINe/Moorings/NISKINE19/')

# %%
project = "NISKINe"

# %% [markdown]
# Save the parameters to `parameters.yml` so we can read them with other functions and do not need to pass them as parameters every time.

# %%
nap.save_params(path=NISKINe_data, project=project)

# %% [markdown]
# ## Read time offsets

# %% [markdown]
# There are two files with time drift information, I must have done this at sea and then on shore again. The second file does not have the instrument type info which makes it easier to read as it is the same format as the time drift file that is used for the SBE37.

# %%
time_offsets = nap.read_time_offsets()

# %%
time_offsets

# %% [markdown]
# ## M1

# %% [markdown] heading_collapsed=true
# ### SN9408

# %% hidden=true
sn = 9408
mooring = 'M1'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=1400, dtop=100, d_interval=16)

# beam 4 seems to be noisier than the other ones.
# turning it off reduces noise in the processed velocities.
# note: beams are indexed zero-based so beam 4 has index 3.
ibad = 3

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
test = xr.open_dataset('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/ADCP/proc/SN9408/M1_9408_old.nc')

# %% hidden=true
test.w.plot(robust=True)

# %% hidden=true
data.w.plot(robust=True)

# %% hidden=true
(test.w-data.w).plot(robust=True)

# %% [markdown] heading_collapsed=true
# ### SN13481

# %% hidden=true
sn = 13481
mooring = 'M1'

# %% [markdown] hidden=true
# The pressure sensor here seems to be off. Not sure if by a constant or by a factor? Why?
#
# Read the pressure time series of this instrument and one of the ADCPs mounted in the float about 700m above this unit (it doesn't matter which of the two as they track each other very well).

# %% hidden=true
dir_data_raw, raw_files, dir_data_out, dir_fig_out = nap.construct_adcp_paths(
    sn, mooring
)
raw1 = gadcp.io.read_raw_rdi(raw_files[0].as_posix(), auxillary_only=True)

# %% hidden=true
raw2 = gadcp.io.read_raw_rdi('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/ADCP/raw/SN9408/09408000.000', auxillary_only=True)

# %% hidden=true
fig, ax = gv.plot.quickfig()
raw1.pressure.plot(linewidth=0.5, ax=ax)
ax.invert_yaxis()
ax.set(ylabel='pressure [dbar]', xlabel='', title='SN13481 pressure record');
gv.plot.png('SN13481_pressure')

# %% [markdown] hidden=true
# The pressure on deck shows noise at much higher amplitude than for the working instrument which makes this look like it is off by some factor.

# %% hidden=true
fig, ax = gv.plot.quickfig()
raw1.pressure[:1000].plot(label="SN13481", ax=ax)
raw2.pressure[:1000].plot(label="SN9408", ax=ax)
ax.legend()
ax.set(ylabel='pressure [dbar]', xlabel='', title='surface pressure');
gv.plot.png('SN13481_surface_pressure')

# %% hidden=true
print(raw1.pressure.isel(time=range(1000)).median())
print(raw2.pressure.isel(time=range(1000)).median())

# %% hidden=true
print(raw1.pressure.isel(time=range(1000)).std())
print(raw2.pressure.isel(time=range(1000)).std())

# %% [markdown] hidden=true
# Maybe we can find a constant scale factor by aligning the minima (where the mooring should be standing upright) of the pressure distributions plus the known offset of the instruments on the mooring.

# %% hidden=true
p1 = raw1.pressure.where(raw1.pressure>800)

# %% hidden=true
p2 = raw2.pressure.where(raw2.pressure>80)

# %% hidden=true
bins = np.arange(100, 600, 1)
fig, ax = gv.plot.quickfig()
p2.plot.hist(bins=bins, ax=ax)
(p1/25.72-706).plot.hist(alpha=0.3, bins=bins, ax=ax)
ax.set(xlim=(100, 300))

# %% hidden=true
fig, ax = gv.plot.quickfig()
raw2.pressure.plot(label="SN9408")
(raw1.pressure/25.72-706).plot(color='r', alpha=0.3, label="SN13481")
# tmp2.pressure.plot()
ax.set(ylim=(500, 100))
ax.legend()
gv.plot.png('SN13481_scaled')

# %% [markdown] hidden=true
# Looks like a scale factor of 1/25.72 creates a pressure time series that lines up with the ADCP above when subtracting 706m of line and chain in between the instrumensts. It also seems reasonable that maximum vertical excursions are larger for the instrument closer to the surface.

# %% [markdown] hidden=true
# There is also an issue with the current directions of this record, they are off when comparing them to the instruments above. Let's compare heading, pitch and roll between 13481 and 9408.

# %% hidden=true
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7.5, 5),
                       constrained_layout=True, sharex=True)
raw1.pitch.plot(ax=ax[0], label='SN13481')
raw2.pitch.plot(ax=ax[0], label='SN9408')
ax[0].legend()
raw1['roll'].plot(ax=ax[1])
raw2['roll'].plot(ax=ax[1])
raw1.heading.plot(ax=ax[2])
raw2.heading.plot(ax=ax[2])
[axi.set(xlabel='', ylim=(-30, 30)) for axi in ax[:2]];

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=2000, dtop=800, d_interval=16)
ibad = None

# %% [markdown] hidden=true
# Here we provide the pressure scale factor to nudge the pressure time series to somewhat realistiv values for the depth gridding.

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None, pressure_scale_factor=1/25.72)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true
# ### SN14408

# %% hidden=true
sn = 14408
mooring = 'M1'

# %% hidden=true
if 0:
    nap.plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=2900, dtop=2700, d_interval=4)
# beam 2 seems to be broken.
# note: beams are indexed zero-based so beam 2 has index 1.
ibad = 1

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true
# ### SN22476

# %% hidden=true
sn = 22476
mooring = 'M1'

# %% hidden=true
if 0:
    nap.plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=1800, dtop=1600, d_interval=4)
ibad = None

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true
# ### SN3109

# %% hidden=true
sn = 3109
mooring = 'M1'

# %% hidden=true
test = xr.open_dataset('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/ADCP/proc/SN3109/M1_3109_old.nc')

# %% hidden=true
new = xr.open_dataset('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/ADCP/proc/SN3109/M1_3109.nc')

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% [markdown] hidden=true
# Data from this ADCP show reflections where the top buoy was in the way. We need to mask bin(s) here.

# %% [markdown] hidden=true
# Read raw data to find out where to mask. Looks like bin 16. Also leaving out the first two bins.

# %% hidden=true
dir_data_raw, raw_files, dir_data_out, dir_fig_out = nap.construct_adcp_paths(
    sn, mooring
)
raw_file = raw_files[0]

# %% hidden=true
raw = gadcp.io.read_raw_rdi(raw_file.as_posix())

# %% hidden=true
fig, ax = gv.plot.quickfig(w=10)
raw.cor.isel(beam=0).gv.tcoarsen(100).gv.tplot(ax=ax)

# %% hidden=true
mc0 = raw.cor.isel(beam=0).mean(dim='time').data
plt.plot(range(len(mc0)), mc0, 'ko')
plt.grid()

# %% hidden=true
mc = raw.cor.groupby('beam').mean(dim='time')
mc.plot(hue='beam', marker='o')
plt.grid()

# %% hidden=true
dgridparams = dict(dbot=600, dtop=0, d_interval=4)
ibad = None

# %% hidden=true
editparams = dict(maskbins=[0, 1, 16])

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, editparams=editparams, ibad=ibad, n_ensembles=None, save_nc=True)

# %% hidden=true
# nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true
# ## M2

# %% [markdown] heading_collapsed=true hidden=true
# ### SN3110

# %% hidden=true
sn = 3110
mooring = 'M2'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=400, dtop=0, d_interval=4)
ibad = None

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN8063

# %% [markdown] hidden=true
# Only a few kilobytes of data.

# %% hidden=true
sn = 8063
mooring = 'M2'

# %% [markdown] heading_collapsed=true hidden=true
# ### SN8065

# %% [markdown] hidden=true
# No pressure time series. Still need to change processing code to allow for external pressure time series input.

# %% hidden=true
sn = 8065
mooring = 'M2'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=400, dtop=0, d_interval=4)
ibad = None

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN22479

# %% hidden=true
sn = 22479
mooring = 'M2'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=2900, dtop=2800, d_interval=4)
ibad = None

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN23615

# %% hidden=true
sn = 23615
mooring = 'M2'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=400, dtop=100, d_interval=4)
ibad = None

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN10219

# %% [markdown] hidden=true
# Raw files for this instruments were split across two memory cards. This can lead to the header in the second file being corrupted as the file is just split at a random point. The two files can be combined in UNIX using `file.000 file.001 > file.all`. I did this for the two files on hand and moved the original raw files into a new subdirectory called `parts`.

# %% hidden=true
sn = 10219
mooring = 'M2'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=900, dtop=300, d_interval=8)
ibad = None

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown]
# ## M3

# %% [markdown] heading_collapsed=true
# ### SN15694

# %% hidden=true
sn = 15694
mooring = 'M3'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=1100, dtop=100, d_interval=16)
ibad = None

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true
# ### SN344

# %% [markdown] hidden=true
# No data for this instrument.

# %% [markdown] heading_collapsed=true
# ### SN8122

# %% hidden=true
sn = 8122
mooring = 'M3'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true
# ### SN12733

# %% hidden=true
sn = 12733
mooring = 'M3'

# %% hidden=true
if 0:
    plot_raw_adcp(mooring, sn)

# %% hidden=true
dgridparams = dict(dbot=1850, dtop=1600, d_interval=4)
ibad = None

# %% hidden=true
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %% hidden=true
nap.plot_adcp(mooring, sn)

# %% [markdown]
# ### SN15339

# %%
sn = 15339
mooring = 'M3'

# %%
if 0:
    plot_raw_adcp(mooring, sn)

# %%
dgridparams = dict(dbot=2950, dtop=2800, d_interval=4)
ibad = None

# %%
nap.process_adcp(mooring, sn, dgridparams, ibad=ibad, n_ensembles=None)

# %%
nap.plot_adcp(mooring, sn)
