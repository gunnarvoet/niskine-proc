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
import rbr

# from pytowyo.io import read_rbr_solo

# %reload_ext autoreload
# %autoreload 2
# %autosave 0
# %config InlineBackend.figure_format = 'retina'

# %% [markdown]
# Path to .rsk files

# %%
rbrdir = Path('/Users/gunnar/Projects/niskin/data/NISKINe/Moorings/NISKINe2020/RBR/raw/')

# %% [markdown]
# Time of pool calibration after recovery

# %%
caltime = np.datetime64('2020-10-09 20:43:00')

# %% [markdown]
# Processing parameters

# %%
data_out = Path('/Users/gunnar/Projects/niskin/data/NISKINe/Moorings/NISKINe2020/RBR/proc/')
figure_out = Path('/Users/gunnar/Projects/niskin/data/NISKINe/Moorings/NISKINe2020/RBR/fig/')

# %% [markdown]
# ## Processed Files

# %%
# this one processed before time cal
solofile = rbrdir.joinpath('072146_20201008_2045.rsk')
solo = rbr.solo.proc(solofile, data_out, figure_out, cal_time=caltime, show_plot=True)

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
# ### 72167
#
# Does not show a time offset. File size smaller than other thermistors - possibly dead before end of deployment?

# %%
# this one processed before time cal
# does not have a time offset
solofile = rbrdir.joinpath('072167_20201008_2230.rsk')
# rsk, data = rbr.solo.read_rsk(solofile)
solo = rbr.solo.proc(solofile, data_out=data_out, figure_out=figure_out, cal_time=caltime, show_plot=True)

# %% [markdown]
# ### 76611
#
# Does not show a time offset (there were problems connecting to the instrument).

# %%
solofile = rbrdir.joinpath('076611_20201009_1500.rsk')

# %%
solo = rbr.solo.proc(solofile, data_out=data_out, figure_out=figure_out, cal_time=caltime, show_plot=True)

# %%
# solofile = rbrdir.joinpath('076611_20201009_0634.rsk')
solofile2 = rbrdir.joinpath('AUTO_076611_20201009 0510.rsk')
# solofile3 = rbrdir.joinpath('AUTO_076611_20201008 2310.rsk')

# %%
test = rbr.solo.read_rsk(solofile2)

# %%
rsk, data = test

# %%
rsk.deployment.download_time

# %%
