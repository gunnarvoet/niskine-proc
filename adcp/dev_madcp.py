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

# %% [markdown] heading_collapsed=true
# #### Imports

# %% hidden=true janus={"all_versions_showing": false, "cell_hidden": false, "current_version": 0, "id": "c8fa3f91f2446", "named_versions": [], "output_hidden": false, "show_versions": false, "source_hidden": false, "versions": []}
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pickle
import gvpy as gv
from pathlib import Path
import gadcp
from gadcp.madcp import npzload

# %reload_ext autoreload
# %autoreload 2
# %config InlineBackend.figure_format = 'retina'
# %autosave 300

# %% [markdown]
# # madcp development
#
# Automate the processing of ADCP data. `gadcp` interfaces with UHs `pycurrents` software.

# %% janus={"all_versions_showing": false, "cell_hidden": false, "current_version": 0, "id": "74a02546e7d3d", "named_versions": [], "output_hidden": false, "show_versions": false, "source_hidden": false, "versions": []}
fname_raw = '/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/ADCP/raw/SN9408/09408000.000'

# %% janus={"all_versions_showing": false, "cell_hidden": false, "current_version": 0, "id": "74a02546e7d3d", "named_versions": [], "output_hidden": false, "show_versions": false, "source_hidden": false, "versions": []}
fname_raw = Path('/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/ADCP/raw/SN9408/09408000.000')

# %%
fname_raw.as_posix()

# %%
'/' in fname_raw.as_posix()

# %% [markdown]
# Pick a shorter time series instead? Maybe later...

# %% janus={"all_versions_showing": false, "cell_hidden": false, "current_version": 0, "id": "74a02546e7d3d", "named_versions": [], "output_hidden": false, "show_versions": false, "source_hidden": false, "versions": []}
# fname_raw = '/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/M1/ADCP/raw/SN22476/22476000.000'

# %% [markdown]
# Provide position and time drift information.

# %%
mooring_positions = xr.open_dataset('/Users/gunnar/Projects/niskine/cruises/cruise1/py/niskine_mooring_locations.nc')

# %%
# position
lon = mooring_positions.sel(mooring=1).lon_actual.data
lat = mooring_positions.sel(mooring=1).lat_actual.data

# %%
# time drift
end_pc   = (2020, 10,  9, 20, 26,  0)
end_adcp = (2020, 10,  9, 20, 23, 29)

# %%
# time drift
end_pc   = (2020, 10,  9, 20, 26,  0)
end_adcp = None

# %%
tmp = driftparams.get("end_adcp", None)

# %%
editparams = dict(
    max_e = 0.2,           # absolute max e
    max_e_deviation = 2,   # max in terms of sigma
    min_correlation = 64,  # 64 is RDI standard
)

# %%
tgridparams = dict(
    # dt_hours=1.0,  #  1.0/4,
    # t0=132,
    # t1 = t1,
    burst_average=True,
)

# %%
dgridparams = dict(
    dbot=1500, dtop=100, d_interval=16
)  # int(self.p_median),  # 50,

# %%
m, mcm, pa, data = gadcp.madcp.proc(fname_raw, lon, lat, editparams, tgridparams, dgridparams, end_pc, end_adcp, n_ensembles=5000, ibad=3)

# %%
fig, ax = gv.plot.quickfig()
data.u.plot()
data.pressure.plot(color='k')
ax.invert_yaxis()

# %%
fig, ax = gv.plot.quickfig()
data.v.plot()
data.pressure.plot(color='k')
ax.invert_yaxis()

# %%
data.npings.plot()
gv.plot.concise_date()

# %% [markdown]
# # Plot raw data

# %% [markdown]
# Also read the raw data.

# %%
test = gadcp.io.read_raw_rdi(fname_raw)

# %%
gadcp.adcp.plot_raw_adcp(test)

# %%
