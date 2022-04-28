# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] heading_collapsed=true
# #### Imports

# %% hidden=true
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

# %config InlineBackend.figure_format = 'retina'


# %% [markdown]
# # NISKINe ADCP data processing

# %% [markdown] heading_collapsed=true
# ## Set parameters

# %% [markdown] hidden=true
# Set the path to your local mooring data directory; this is the directory level that contains folders `M1`, `M2`, and `M3`, for individual moorings.

# %% hidden=true
NISKINe_data = Path('/Users/gunnar/Projects/niskine/data/NISKINe/Moorings/NISKINE19/')

# %% hidden=true
project = "NISKINe"

# %% [markdown] hidden=true
# Save the parameters to `parameters.yml` so we can read them with other functions and do not need to pass them as parameters every time.

# %% hidden=true
nap.save_params(path=NISKINe_data, project=project)

# %% [markdown] hidden=true
# Set the following to `True` if you want to run the raw data plots.

# %% hidden=true
plot_raw = False

# %% [markdown] hidden=true
# Standard processing parameters are
# ```
# min_correlation = 64
# max_e = 0.2
# pg_limit = 50
# ```

# %% [markdown] heading_collapsed=true
# ## Read time offsets

# %% [markdown] hidden=true
# There are two files with time drift information, I must have done this at sea and then on shore again. The second file does not have the instrument type info which makes it easier to read as it is the same format as the time drift file that is used for the SBE37.

# %% hidden=true
time_offsets = nap.read_time_offsets()

# %% hidden=true
time_offsets

# %% [markdown] heading_collapsed=true
# ## M1

# %% [markdown] heading_collapsed=true hidden=true
# ### SN9408 (reprocessed)

# %% [markdown] hidden=true
# Data in bins 6 to about 20 are noisy due to fishing long line entangled in the mooring. This matches with notes from the mooring recovery showing long line to about 200m from the instrument. Beam 4 is noisier than beams 1 to 3. We still use the 4-beam solution as otherwise we don't have an error velocity to filter out bad data. A comparison with a 3-beam solution shows that this is the better approach.

# %% [markdown] hidden=true
# Ideally, in this situation we would like to calculate error velocities from all four beams but then use only three beams to calculate velocities. We could still use the error velocity to filter out bad data. I will try this by running the processing first with all four beams but not applying any pg_limit criterion, just to obtain the error velocity. In a next step I will generate a three beam solution and then finally apply the pg limit. Update: Tried this and it didn't look very good so scrap this idea.

# %% [markdown] hidden=true
# We bump up the `pg_limit` to 70 to be a bit more aggressive in filtering out bad data.

# %% hidden=true
sn = 9408
mooring = 'M1'

# %% hidden=true
dgridparams = dict(dbot=1400, dtop=100, d_interval=16)

# beam 4 seems to be noisier than the other ones.
# note: beams are indexed zero-based so beam 4 has index 3.
ibad = 3
# we do want error velocities though (see notes above) and thus will not exclude beam 4
ibad = None

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams, ibad=ibad)

# %% hidden=true
if plot_raw:
    a.plot_raw_adcp()

# %% hidden=true
if plot_raw:
    a.plot_echo_stats()

# %% hidden=true
# binmask = a.generate_binmask([0, 1, 16])
# editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
editparams = dict(max_e=0.2, pg_limit=70, min_correlation=64)
a.parse_editparams(editparams)

# %% hidden=true
a.editparams

# %% [markdown] hidden=true
# Burst-average.

# %% hidden=true
a.burst_average_ensembles(4500, 5000)

# %% hidden=true
fig, ax = gv.plot.quickfig(w=10)
ax = a.ds.u.dropna(dim='z', how='all').gv.tplot(ax=ax, robust=True)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% [markdown] hidden=true
# Note the spike in pressure on October 7th, 2019. Was this somebody yanking on the long line?

# %% hidden=true
fig, ax = gv.plot.quickfig(w=10)
ax = pp.pressure.sel(time=slice('2019-10-06', '2019-10-09')).gv.tplot(ax=ax)

# %% [markdown] hidden=true
# Let's also generate a version where beam 4 has been masked.

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams, ibad=3)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data(name_suffix='beam4masked')

# %% [markdown] heading_collapsed=true hidden=true
# ### SN13481 (reprocessed)

# %% hidden=true
sn = 13481
mooring = 'M1'

# %% [markdown] heading_collapsed=true hidden=true
# #### Pressure sensor issue

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
raw2 = gadcp.io.read_raw_rdi('/Users/gunnar/Projects/niskine/data/NISKINe/Moorings/NISKINE19/M1/ADCP/raw/SN9408/09408000.000', auxillary_only=True)

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

# %% [markdown] heading_collapsed=true hidden=true
# #### Process data

# %% hidden=true
dgridparams = dict(dbot=2000, dtop=800, d_interval=16)
ibad = None

# %% [markdown] hidden=true
# Here we provide the pressure scale factor to nudge the pressure time series to somewhat realistiv values for the depth gridding.

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams, ibad=ibad, pressure_scale_factor=1/25.72)

# %% hidden=true
if plot_raw:
    a.plot_raw_adcp()

# %% hidden=true
if plot_raw:
    a.plot_echo_stats()

# %% hidden=true
editparams = dict(max_e=0.2, pg_limit=50, min_correlation=64)
a.parse_editparams(editparams)

# %% hidden=true
a.editparams

# %% [markdown] hidden=true
# Burst-average.

# %% hidden=true
a.burst_average_ensembles(3800, 4000)

# %% hidden=true
fig, ax = gv.plot.quickfig(w=10)
ax = a.ds.u.dropna(dim='z', how='all').gv.tplot(ax=ax, robust=True)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN14408 (reprocessed)

# %% hidden=true
sn = 14408
mooring = 'M1'

# %% hidden=true
dgridparams = dict(dbot=2900, dtop=2700, d_interval=4)
# beam 2 seems to be broken.
# note: beams are indexed zero-based so beam 2 has index 1.
ibad = 1

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams, ibad=ibad)

# %% hidden=true
if plot_raw:
    a.plot_raw_adcp()

# %% hidden=true
a.plot_echo_stats()

# %% [markdown] hidden=true
# We turn off the correlation-based data quality check as correlation drops quickly. We also can't use error velocity due to the broken beam. Thus, we basically use the raw, unedited data. What I don't understand is what determines which bins have data at all in the raw data file.

# %% hidden=true
binmask = a.generate_binmask([0, 6])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=30, min_correlation=0)
a.parse_editparams(editparams)

# %% hidden=true
a.editparams

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.ds.pg.gv.tplot()

# %% hidden=true
a.ds.u.gv.tplot()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)
data.close()

# %% [markdown] heading_collapsed=true hidden=true
# ### SN22476 (reprocessed)

# %% hidden=true
sn = 22476
mooring = 'M1'

# %% hidden=true
dgridparams = dict(dbot=1800, dtop=1600, d_interval=4)
ibad = None

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
binmask = a.generate_binmask([0, 1, 2])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN3109 (reprocessed)

# %% [markdown] hidden=true
# Top ADCP on M1, 300kHz. The steel buoy about 70m away shows up in the data.

# %% hidden=true
sn = 3109
mooring = 'M1'

# %% hidden=true
# dgridparams = dict(dbot=1700, dtop=1000, d_interval=16)
# now generating top and bot automatically based on median depth of ADCP
# dgridparams = dict(d_interval=16)
dgridparams = dict(dbot=600, dtop=16, d_interval=4)

# %% [markdown] hidden=true
# Generate a `ProcessNISKINeADCP` instance that is based off the `gadcp.madcp.ProcessADCP` object.

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams)

# %% hidden=true
a.meta_data

# %% [markdown] hidden=true
# Plot beam statistics to find ADCP bins that need to be excluded. Reflection from the mooring top float can be seen in depth bin 16.

# %% hidden=true
a.plot_echo_stats()

# %% [markdown] hidden=true
# We mask the first two bins and the one with reflections from the surface float.

# %% hidden=true
binmask = a.generate_binmask([0, 1, 16])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.editparams

# %% [markdown] hidden=true
# Burst-average. Interpolate over the masked bin 16.

# %% hidden=true
a.burst_average_ensembles(51500, 52500, interpolate_bin=16)

# %% hidden=true
fig, ax = gv.plot.quickfig(w=10)
ax = a.ds.u.dropna(dim='z', how='all').gv.tplot(ax=ax, robust=True)

# %% hidden=true
a.burst_average_ensembles(interpolate_bin=16)

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true
# ## M2

# %% [markdown] heading_collapsed=true hidden=true
# ### SN3110 (reprocessed)

# %% [markdown] hidden=true
# Top ADCP on M2, 300kHz. The steel buoy about 50m away shows up in the data.

# %% hidden=true
sn = 3110
mooring = 'M2'

# %% hidden=true
# dgridparams = dict(dbot=1700, dtop=1000, d_interval=16)
# now generating top and bot automatically based on median depth of ADCP
# dgridparams = dict(d_interval=16)
dgridparams = dict(dbot=400, dtop=0, d_interval=4)

# %% [markdown] hidden=true
# Generate a `ProcessNISKINeADCP` instance that is based off the `gadcp.madcp.ProcessADCP` object.

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams)

# %% hidden=true
a.meta_data

# %% [markdown] hidden=true
# Plot beam statistics to find ADCP bins that need to be excluded. Reflection from the mooring top float can be seen in depth bin 16.

# %% hidden=true
a.plot_echo_stats()

# %% [markdown] hidden=true
# We mask the first bin and the one with reflections from the surface float.

# %% hidden=true
binmask = a.generate_binmask([0, 11])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.editparams

# %% [markdown] hidden=true
# Burst-average. Interpolate over the masked bin 11.

# %% hidden=true
a.burst_average_ensembles(51500, 52500, interpolate_bin=11)

# %% hidden=true
fig, ax = gv.plot.quickfig(w=10)
ax = a.ds.u.dropna(dim='z', how='all').gv.tplot(ax=ax, robust=True)

# %% hidden=true
a.raw.amp.where(a.raw.amp<80, other=0).isel(beam=1, time=slice(400000,410000)).plot()

# %% hidden=true
a.raw.cor.isel(beam=1, time=slice(400000,403000)).plot()

# %% hidden=true
a.raw.vel.isel(beam=1, time=slice(400000,410000)).plot()

# %% hidden=true
a.raw.amp.isel(beam=1, time=slice(40000,50000)).plot()

# %% hidden=true
a.burst_average_ensembles(interpolate_bin=11)

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true hidden=true
# ### SN8063 (no data)

# %% [markdown] hidden=true
# Only a few kilobytes of data.

# %% hidden=true
sn = 8063
mooring = 'M2'

# %% [markdown] heading_collapsed=true hidden=true
# ### SN8065 (reprocessed)

# %% [markdown] hidden=true
# No pressure time series. Still need to change processing code to allow for external pressure time series input.

# %% [markdown] hidden=true
# Pressure time series from SBE37 4922.

# %% hidden=true
p = xr.open_dataset('/Users/gunnar/Projects/niskine/data/NISKINe/Moorings/NISKINE19/M2/SBE37/proc/SN4922/SBE37_4922_NISKINE.nc').p

# %% hidden=true
ax = p.gv.tcoarsen().gv.tplot()
ax.invert_yaxis()

# %% hidden=true
sn = 8065
mooring = 'M2'

# %% hidden=true
dgridparams = dict(dbot=500, dtop=0, d_interval=4)
ibad = None

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams, pressure=p)

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
binmask = a.generate_binmask([0, 1])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true hidden=true
# ### SN22479 (reprocessed)

# %% hidden=true
sn = 22479
mooring = 'M2'

# %% hidden=true
# dgridparams = dict(dbot=2900, dtop=2800, d_interval=4)

# %% [markdown] hidden=true
# Use depth gridding parameters determined by `gadcp`.

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn)

# %% hidden=true
a.default_dgridparams

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
binmask = a.generate_binmask([0])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true hidden=true
# ### SN23615 (reprocessed)

# %% hidden=true
sn = 23615
mooring = 'M2'

# %% hidden=true
dgridparams = dict(dbot=400, dtop=100, d_interval=4)
ibad = None

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams)

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
editparams = dict(max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true hidden=true
# ### SN10219 (reprocessed)

# %% [markdown] hidden=true
# Raw files for this instruments were split across two memory cards. This can lead to the header in the second file being corrupted as the file is just split at a random point. The two files can be combined in UNIX using `file.000 file.001 > file.all`. I did this for the two files on hand and moved the original raw files into a new subdirectory called `parts`.

# %% hidden=true
sn = 10219
mooring = 'M2'

# %% hidden=true
# dgridparams = dict(dbot=1700, dtop=1000, d_interval=16)
# now generating top and bot automatically based on median depth of ADCP
# dgridparams = dict(d_interval=16)
dgridparams = dict(dbot=900, dtop=300, d_interval=8)

# %% [markdown] hidden=true
# Generate a `ProcessNISKINeADCP` instance that is based off the `gadcp.madcp.ProcessADCP` object.

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams)

# %% hidden=true
a.meta_data

# %% [markdown] hidden=true
# Plot beam statistics to find ADCP bins that need to be excluded.

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
# binmask = a.generate_binmask([0, 1, 16])
editparams = dict(max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.editparams

# %% [markdown] hidden=true
# Burst-average.

# %% hidden=true
a.burst_average_ensembles(41500, 42500)

# %% hidden=true
fig, ax = gv.plot.quickfig(w=10)
ax = a.ds.u.dropna(dim='z', how='all').gv.tplot(ax=ax, robust=True)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true
# ## M3

# %% [markdown] heading_collapsed=true hidden=true
# ### SN15694 (reprocessed)

# %% hidden=true
sn = 15694
mooring = 'M3'

# %% hidden=true
dgridparams = dict(dbot=1100, dtop=100, d_interval=16)

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams)

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
binmask = a.generate_binmask([0])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true hidden=true
# ### SN344 (no data)

# %% [markdown] hidden=true
# No data for this instrument.

# %% [markdown] heading_collapsed=true hidden=true
# ### SN8122 (reprocessed)

# %% hidden=true
sn = 8122
mooring = 'M3'

# %% [markdown] hidden=true
# Pressure time series from SBE37 3638.

# %% hidden=true
p = xr.open_dataset('/Users/gunnar/Projects/niskine/data/NISKINe/Moorings/NISKINE19/M3/SBE37/proc/SN3638/SBE37_3638_NISKINE.nc').p

# %% hidden=true
ax = p.gv.tcoarsen().gv.tplot()
ax.invert_yaxis()

# %% hidden=true
dgridparams = dict(dbot=1100, dtop=800, d_interval=4)

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams, pressure=p)

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
binmask = a.generate_binmask([0])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true hidden=true
# ### SN12733 (reprocessed)

# %% hidden=true
sn = 12733
mooring = 'M3'

# %% hidden=true
dgridparams = dict(dbot=1850, dtop=1600, d_interval=4)

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams)

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
binmask = a.generate_binmask([0])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()

# %% [markdown] heading_collapsed=true hidden=true
# ### SN15339 (reprocessed)

# %% hidden=true
sn = 15339
mooring = 'M3'

# %% hidden=true
dgridparams = dict(dbot=2950, dtop=2800, d_interval=4)

# %% hidden=true
a = nap.ProcessNISKINeADCP(mooring, sn, dgridparams=dgridparams)

# %% hidden=true
a.plot_echo_stats()

# %% hidden=true
binmask = a.generate_binmask([0])
editparams = dict(maskbins=binmask, max_e=0.2, pg_limit=50)
a.parse_editparams(editparams)

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.save_averaged_data()

# %% hidden=true
data = nap.plot_adcp(mooring, sn)

# %% hidden=true
if plotraw:
    a.plot_raw_adcp()
