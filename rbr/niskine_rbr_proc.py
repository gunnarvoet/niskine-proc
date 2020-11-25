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
# # NISKINe RBR Solo Processing

# %%
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xarray as xr
from pathlib import Path
import pyrsktools
import os

import gvpy as gv
import rbrmoored as rbr

# %reload_ext autoreload
# %autoreload 2
# %autosave 300
# %config InlineBackend.figure_format = 'retina'

# %% [markdown]
# Path to .rsk files

# %%
rbrdir = Path('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/RBRSolo/raw/')

# %% [markdown]
# Time of pool calibration after recovery

# %%
caltime = np.datetime64('2020-10-09 20:43:00')

# %% [markdown]
# Processing parameters

# %%
data_out = Path('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/RBRSolo/proc/')
figure_out = Path('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/RBRSolo/fig')
# Create directories if needed
for d in [data_out, figure_out]:
    d.mkdir(exist_ok=True)

# %% [markdown]
# ## Processed Files

# %%
solofile = rbrdir.joinpath('072214_20201010_0320.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072149_20201010_0348.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath("072155_20201010_0405.rsk")
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072153_20201010_0424.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072206_20201010_0446.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072175_20201010_0505.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072194_20201010_0525.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072219_20201010_0545.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072147_20201010_0606.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072174_20201010_0625.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072216_20201010_0646.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072202_20201010_0709.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072196_20201010_0800.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('076608_20201010_0825.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072158_20201010_0845.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072183_20201010_0905.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072164_20201010_0928.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072187_20201010_0947.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072159_20201010_1009.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072215_20201010_1030.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072178_20201010_1047.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072180_20201010_1141.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072161_20201010_1434.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072186_20201010_1457.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072160_20201010_1541.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072152_20201010_1602.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072210_20201010_1648.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %%
solofile = rbrdir.joinpath('072208_20201010_1753.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

# %% [markdown]
# ## Problem Childs

# %% [markdown]
# ### 72146
#
# The noted time offset is wrong - likely due to the wrong time on the download computer. The time on the download computer was about 42s behind UTC (see notes for SBE56).

# %%
# this one processed before time cal
solofile = rbrdir.joinpath('072146_20201008_2045.rsk')
solo = rbr.solo.proc(solofile, show_plot=False, apply_time_offset=False)

# %% [markdown]
# Subtracting 42s from the time offset (54843ms) leaves about 12s. This seems to make more sense when comparing the temperature signal at mooring release time with thermistors below.

# %%
below2 = xr.open_dataarray('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/RBRSolo/proc/072180_20201010_1141.nc')

# %%
below3 = xr.open_dataarray('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/RBRSolo/proc/072187_20201010_0947.nc')

# %%
below4 = xr.open_dataarray('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/RBRSolo/proc/072210_20201010_1648.nc')

# %%
# timesel = slice('2020-10-05 00:00', '2020-10-05 23:59')
# fig, ax = gv.plot.quickfig()
# solo.sel(time=timesel).plot(label=solo.attrs['SN'])
# below2.sel(time=timesel).plot(label=below2.attrs['SN'])
# below3.sel(time=timesel).plot(label=below3.attrs['SN'])
# below4.sel(time=timesel).plot(label=below4.attrs['SN'])
# ax.legend()

# %%
solo.attrs['time drift in ms'] = 12000

# %%
solo = rbr.solo.time_offset(solo)

# %% [markdown]
# Looks ok. Save.

# %%
rbr.solo.save_nc(solo, data_out=data_out)

# %%
rbr.solo.plot(solo, figure_out=figure_out)

# %%
sn72146 = xr.open_dataarray('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/RBRSolo/proc/072146_20201008_2045.nc')

# %% [markdown]
# ### 72167
#
# Does not show a time offset. File size smaller than other thermistors.

# %%
# this instrument was downloaded before the clock calibration,
# so no reference time exists
solofile = rbrdir.joinpath('072167_20201008_2230.rsk')
solo = rbr.solo.proc(solofile, show_plot=True)

# %% [markdown]
# Compare with 72180 (20m below). 72146 (10m below) would be closer, but it also was downloaded on the faulty computer and may not be as accurate.

# %%
# timesel = slice('2020-10-05 00:00', '2020-10-05 23:59')
# fig, ax = gv.plot.quickfig()
# solo.sel(time=timesel).plot(label=solo.attrs['SN'])
# sn72146.sel(time=timesel).plot(label=sn72146.attrs['SN'])
# below2.sel(time=timesel).plot(label=below2.attrs['SN'])
# below3.sel(time=timesel).plot(label=below3.attrs['SN'])
# below4.sel(time=timesel).plot(label=below4.attrs['SN'])
# ax.legend()

# %% [markdown]
# Comparing with instruments below, it appears there is not much of a time drift to correct for.

# %%
rbr.solo.save_nc(solo, data_out=data_out)

# %%
rbr.solo.plot(solo, figure_out=figure_out)

# %%
sn72167 = xr.open_dataarray('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/RBRSolo/proc/072167_20201008_2230.nc')

# %% [markdown]
# ### 76611
#
# Does not show a time offset (there were problems connecting to the instrument).

# %%
solofile = rbrdir.joinpath('076611_20201009_1500.rsk')

# %%
solo = rbr.solo.proc(solofile, show_plot=True)

# %% [markdown]
# Compare with other thermistors. 

# %%
# timesel = slice('2020-10-08 09:20', '2020-10-08 10:55')
# # timesel = slice('2020-10-05 00:00', '2020-10-05 23:59')
# fig, ax = gv.plot.quickfig()
# solo.sel(time=timesel).plot(label=solo.attrs['SN'])
# sn72146.sel(time=timesel).plot(label=sn72146.attrs['SN'])
# sn72167.sel(time=timesel).plot(label=sn72167.attrs['SN'])
# below2.sel(time=timesel).plot(label=below2.attrs['SN'])
# below3.sel(time=timesel).plot(label=below3.attrs['SN'])
# below4.sel(time=timesel).plot(label=below4.attrs['SN'])
# ax.legend()

# %% [markdown]
# Looks like a clock drift of 10s.

# %%
solo.attrs['time drift in ms'] = 10000

# %%
solo = rbr.solo.time_offset(solo)

# %% [markdown]
# Looks ok. Save.

# %%
rbr.solo.save_nc(solo, data_out=data_out)

# %%
rbr.solo.plot(solo, figure_out=figure_out)
