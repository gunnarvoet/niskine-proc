# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# #### Imports

# %%
# # %load /Users/gunnar/Projects/python/standard_imports.py
# %matplotlib inline
import scipy as sp
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import xarray as xr
import gsw
from munch import *

# import own modules (install from https://github.com/gunnarvoet/pythonlib))
import gvpy as gv

# %config InlineBackend.figure_format = 'retina'
# %reload_ext autoreload
# %autoreload 2

# %% [markdown]
# # NISKINe Mooring Triangulation

# %% [markdown]
# ## Sounding results

# %% [markdown]
# Create data structure

# %%
moorings = ['m1', 'm2', 'm3']

# %%
# Create data structure with dot access
s = Munch()
for mi in moorings:
    s[mi] = Munch()
    s[mi].sounding = Munch()
    s[mi].actual_location = Munch()
    s[mi].planned_location = Munch()

# %% [markdown]
# Add triangulation results below

# %%
s.m1.sounding.lat = 59 + np.array([5.606, 5.420, 6.973]) / 60
s.m1.sounding.lon = -21 - np.array([13.722, 10.402, 11.726]) / 60
s.m1.sounding.bdepth = 2881
s.m1.sounding.sr = np.array([3468, 3459, 3325])
s.m1.sounding.hdist = np.sqrt(s.m1.sounding.sr**2 - s.m1.sounding.bdepth**2);
s.m1.planned_location.lon = -21-12/60
s.m1.planned_location.lat = 59.1

# %%
s.m2.sounding.lat = 58 + np.array([58.209, 56.933, 58.575]) / 60
s.m2.sounding.lon = -21 - np.array([13.814, 11.633, 10.577]) / 60
s.m2.sounding.bdepth = 2894
s.m2.sounding.sr = np.array([3504, 3464, 3321])
s.m2.sounding.hdist = np.sqrt(s.m2.sounding.sr**2 - s.m2.sounding.bdepth**2);
s.m2.planned_location.lon = -21.2
s.m2.planned_location.lat = 58.9651

# %%
s.m3.sounding.lat = 59 + np.array([02.892, 01.875, 01.156]) / 60
s.m3.sounding.lon = -21 - np.array([26.281, 23.676, 26.741]) / 60
s.m3.sounding.bdepth = 2900
s.m3.sounding.sr = np.array([3713, 3180, 3536])
s.m3.sounding.hdist = np.sqrt(s.m3.sounding.sr**2 - s.m3.sounding.bdepth**2);
s.m3.planned_location.lon = -21-25.61/60
s.m3.planned_location.lat = 59+1.9486/60


# %% [markdown]
# ## Triangulation routine

# %%
def triangulate(snd, plan):
    x1, y1, dist_1 = ( snd.lon[0], snd.lat[0], snd.hdist[0])
    x2, y2, dist_2 = ( snd.lon[1], snd.lat[1], snd.hdist[1])
    if len(snd.lon)>2:
        x3, y3, dist_3 = ( snd.lon[2], snd.lat[2], snd.hdist[2])

    # Define a function that evaluates the equations
    def equations(guess):
        x, y, r = guess
        if len(snd.lon)>2:
            return (
                gsw.distance([x, x1], [y, y1], p=0)[0] - (dist_1 - r ),
                gsw.distance([x, x2], [y, y2], p=0)[0] - (dist_2 - r ),
                gsw.distance([x, x3], [y, y3], p=0)[0] - (dist_3 - r ))
        else:
            return (
                gsw.distance([x, x1], [y, y1], p=0)[0] - (dist_1 - r ),
                gsw.distance([x, x2], [y, y2], p=0)[0] - (dist_2 - r ))
    
    if 'lon' in plan:
        initial_guess = (plan.lon, plan.lat, 20)
    else:
        initial_guess = (snd.lon.mean(), snd.lat.mean(), 10)

    results = least_squares(equations, initial_guess)

#     print(gv.ocean.lonlatstr(lon=results.x[0], lat=results.x[1]))
    return results.x


# %%
for mi in moorings:
    s[mi].actual_location.lon, s[mi].actual_location.lat, s[mi].actual_location.error = triangulate(s[mi].sounding, s[mi].planned_location)

# %%
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(10, 5))
if 1:
    for axi, (k, si) in zip(ax, s.items()):
        axi.plot(si.sounding.lon, si.sounding.lat, 'ko')
        axi.plot(si.actual_location.lon, si.actual_location.lat, 'ro')
        axi.plot(si.planned_location.lon, si.planned_location.lat, 'bo')
else:
    ax[1].plot(s['m2'].sounding.lon, s['m2'].sounding.lat, 'ko')
    ax[1].plot(s['m2'].actual_location.lon, s['m2'].actual_location.lat, 'ro')
    ax[1].plot(s.m2.planned_location.lon, s.m2.planned_location.lat, 'bo')
    ax[2].plot(s['m3'].sounding.lon, s['m3'].sounding.lat, 'ko')
    ax[2].plot(s['m3'].actual_location.lon, s['m3'].actual_location.lat, 'ro')
    ax[2].plot(s.m3.planned_location.lon, s.m3.planned_location.lat, 'bo')
# ax.plot(results.x[0], results.x[1], 'ro')


# %%
for k, si in s.items():
    s[k]['offset'] = gsw.distance(np.array([si.planned_location.lon, si.actual_location.lon]), np.array([si.planned_location.lat, si.actual_location.lat]), p=0)[0]

# %%
for k, si in s.items():
    print(si.offset)

# %% [markdown]
# Print actual mooring locations

# %%
for k, si in s.items():
    print(k, ':', gv.ocean.lonlatstr(si.actual_location.lon, si.actual_location.lat))

# %%
for k, si in s.items():
    print(f"{k} : {si.actual_location.lon:.4f} {si.actual_location.lat:.4f}")

# %% [markdown]
# Save planned and actual locations to a file.

# %%
m = xr.Dataset(coords={'mooring': ('mooring', np.array([1, 2, 3]))},
               data_vars={'name': ('mooring', ['M1', 'M2', 'M3'])})
a = []
for k, si in s.items():
    a.append(si.actual_location.lon)
m['lon_actual'] = (['mooring'], a)
a = []
for k, si in s.items():
    a.append(si.actual_location.lat)
m['lat_actual'] = (['mooring'], a)
a = []
for k, si in s.items():
    a.append(si.planned_location.lon)
m['lon_planned'] = (['mooring'], a)
a = []
for k, si in s.items():
    a.append(si.planned_location.lat)
m['lat_planned'] = (['mooring'], a)
a = []
for k, si in s.items():
    a.append(si.sounding.bdepth)
m['depth_planned'] = (['mooring'], a)


# %%
m.to_netcdf('triangulation_results.nc')
