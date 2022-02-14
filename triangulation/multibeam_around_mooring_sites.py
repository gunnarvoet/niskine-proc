# -*- coding: utf-8 -*-
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
# %matplotlib inline
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import xarray as xr
import gsw
import cartopy.crs as ccrs
from pathlib import Path

import gvpy as gv

# %reload_ext autoreload
# %autoreload 2
# %config InlineBackend.figure_format = 'retina'
# %autosave 300

# %% [markdown]
# # Read Smith & Sandwell

# %%
lonr = np.array([-26, -18])
latr = np.array([58, 64.5])

# %%
ss = gv.ocean.smith_sandwell(lonr, latr)
ss = -ss


# %%
def gl_format(ax):
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
    gl = ax.gridlines(draw_labels=True)
    gl.top_labels=False
    gl.xlines=False
    gl.right_labels=False
    gl.ylines=False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return gl


# %%
# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10), projection=ccrs.PlateCarree())
fig = plt.figure(figsize=(10, 5))
ax = plt.axes(projection=ccrs.PlateCarree())
hc = ax.contourf(ss.lon, ss.lat, ss.data, levels=np.arange(0, 4100, 100), cmap='Blues', vmin=0, vmax=3500)
# hcl = ax.contour(ss.lon, ss.lat, ss.data, levels=[2750, 3050], colors='w')
gl = gl_format(ax)
hcb = plt.colorbar(hc)
hcb.ax.invert_yaxis()

# %% [markdown]
# # Mooring locations

# %%
M1 = (-21.2, 59.1)
M2 = (-21.2, 58.9651) #(-21.463, 58.865)
M3 = (-21-25.61/60, 59+1.9486/60) #(-21.726, 59.1)

# %%
M = {'M1': M1, 'M2': M2, 'M3': M3}

# %% [markdown]
# Now that we have the mooring deployed also add actual locations

# %%
mact = xr.open_dataset('triangulation_results.nc')

# %%
for g, mi in mact.groupby('mooring'):
    M['M'+g.astype(str)+'_actual'] = [mi.lon_actual.data, mi.lat_actual.data]

# %%
M

# %% [markdown]
# # Multibeam data

# %%
mbfile = '/Users/gunnar/Projects/niskine/cruises/cruise1/proc/mb/grd/all_100_-23_-21_58_61.nc'

# %%
b = xr.open_dataset(mbfile)

# %%
b.z.plot()

# %%
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
b.z.plot(vmin=2800, vmax=3000)
ax.set(xlim=(-21.5, -21.1), ylim=(58.9, 59.2))
for k, m in M.items():
    ax.plot(m[0], m[1], 'ro')
ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(6))
ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(6))
plt.savefig('mb_around_mooring_sites.png', dpi=200, bbox_inches='tight')


# %%
def extract_around_mooring_site(m, dx=0.01):
    lon = m[0]
    lat = m[1]
    lonr = lon + np.array([-dx, dx])
    latr = lat + np.array([-dx, dx])
    out = b.z.isel(x=((b.x>lonr.min()) & (b.x<lonr.max())),
                   y=((b.y>latr.min()) & (b.y<latr.max())))
    return out


# %%
def plot_bathy_around_mooring_site(mii, savename):
    mi = M[mii]
    mib = extract_around_mooring_site(mi, dx=0.02)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    mib.plot(robust=True, ax=ax)
    plt.plot(mi[0], mi[1], 'ro')
    plt.plot(M[mii+'_actual'][0], M[mii+'_actual'][1], 'wo')
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(6))
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(6))
    ax.text(0.1, 0.9, mii, transform=ax.transAxes, color='w', fontweight='bold')
    plt.savefig(savename+'.png', dpi=200, bbox_inches='tight')


# %%
plot_bathy_around_mooring_site('M1', 'mb_around_m1')

# %%
plot_bathy_around_mooring_site('M2', 'mb_around_m2')

# %%
plot_bathy_around_mooring_site('M3', 'mb_around_m3')

# %%
b.z.interp(x=M1[0], y=M1[1])

# %%
m1b.median()

# %%
m2b = extract_around_mooring_site(M2, dx=0.02)

# %%
m2b.plot()
plt.plot(M2[0], M2[1], 'ro')

# %%
b.z.interp(x=M2[0], y=M2[1])

# %%
m2b.median()

# %% [markdown]
# M3

# %%
m3b = extract_around_mooring_site(M3, dx=0.02)

# %%
m3b.plot()
plt.plot(M3[0], M3[1], 'ro')

# %%
m3b.median()

# %%
b.z.interp(x=M3[0], y=M3[1])

# %%
M3

# %% [markdown]
# M3 CTD cast went to about 2938 dbar with 2m on the altimeter. 59° 2.393, 21° 24.301

# %%
m3ctdpos = (-21-24.301/60, 59+2.393/60)

# %%
gsw.z_from_p(2938, M3[1]) - 2

# %%
M3[1]

# %%
m3b2 = extract_around_mooring_site(M3, dx=0.04)

# %%
m3b2.plot()
plt.plot(M3[0], M3[1], 'ro')
plt.plot(m3ctdpos[0], m3ctdpos[1], 'ko')

# %%
b.z.interp(x=m3ctdpos[0], y=m3ctdpos[1])

# %%
m3bctd = extract_around_mooring_site(m3ctdpos)

# %%
m3bctd.plot()
plt.plot(m3ctdpos[0], m3ctdpos[1], 'ro')

# %%
m3bctd.median()

# %%
M3

# %% [markdown]
# Extract depth at actual mooring locations

# %%
mloc = xr.open_dataset('triangulation_results.nc')

# %%
mloc

# %%
for _, mi in mloc.groupby('mooring'):
    print('planned depth:', b.z.interp(x=mi.lon_planned, y=mi.lat_planned).data)
    print('actual depth:', b.z.interp(x=mi.lon_actual, y=mi.lat_actual).data)


# %% [markdown]
# Add actual depth to the mooring location data structure.

# %%
dep = []
for _, mi in mloc.groupby('mooring'):
    dep.append(b.z.interp(x=mi.lon_actual, y=mi.lat_actual).data)

dep = np.round(np.squeeze(dep), decimals=0)

# %%
mloc['depth_actual'] = (['mooring'], dep)

# %%
mloc.depth_actual

# %%
mloc.close()

# %%
mloc.to_netcdf('niskine_mooring_locations.nc')

# %%
