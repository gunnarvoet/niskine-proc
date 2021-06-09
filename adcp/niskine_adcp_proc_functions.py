#!/usr/bin/env python
# coding: utf-8

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
from pathlib import Path
import datetime
import yaml

import gvpy as gv
import gadcp

# Set paths
# NISKINe_data = Path("/Users/gunnar/Projects/niskine/data/Moorings/NISKINE19/")

def save_params(path, project):
    """Save parameters to local yaml file for easy access via other functions.

    Parameters
    ----------
    path : str
        Path to NISKINe data directory. This is the directory level that
        contains folders `M1`, `M2`, and `M3`, for individual moorings.
    project : str
        Project name.
    """
    out = dict(path=path.as_posix(), project=project)
    with open("parameters.yml", "w") as outfile:
        yaml.dump(out, outfile, default_flow_style=False)


def read_params():
    """Read yaml parameters file saved with save_params().

    Returns
    -------
    params : dict
        Parameters
    """
    try:
        with open("parameters.yml") as file:
            params = yaml.safe_load(file)
        return params
    except IOError as x:
        print(x)
        print(
            "run save_params() first to save the path to the data directory\nas a yaml parameter file"
        )


def construct_adcp_paths(sn, mooring):
    """ Generate data paths depending on mooring / instrument serial number.

    Parameters
    ----------
    sn : int
        ADCP serial number.
    mooring : str
        Mooring ID.

    Returns
    -------
    dir_data_raw : PosixPath
        Path to raw ADCP data
    raw_files : list
        Path(s) to raw ADCP data files
    dir_data_out : PosixPath
        Path to processed data
    dir_fig_out : PosixPath
        Path for saving figures

    Notes
    -----
    Some ADCPs have more than one data file, but in many cases the extra files
    have zero size. We'll generate a list with all file names and then throw
    those out that are smaller than just a few kb.
    """

    params = read_params()
    NISKINe_data = Path(params["path"])
    dir_data_raw = NISKINe_data.joinpath(mooring).joinpath(
        "ADCP/raw/SN{}".format(sn)
    )
    # list all raw files
    all_raw_files = list(sorted(dir_data_raw.glob("*.00*")))
    # only files larger than about 10kB
    raw_files = [file for file in all_raw_files if file.stat().st_size > 1e4]
    dir_data_out = NISKINe_data.joinpath(mooring).joinpath(
        "ADCP/proc/SN{}".format(sn)
    )
    if not dir_data_out.exists():
        dir_data_out.mkdir()
    dir_fig_out = NISKINe_data.joinpath(mooring).joinpath("ADCP/fig/")
    if not dir_fig_out.exists():
        dir_fig_out.mkdir()

    return dir_data_raw, raw_files, dir_data_out, dir_fig_out


def read_time_offsets():
    """Read ascii file with ADCP time offsets and return as pandas data structure.

    Returns
    -------
    time_offsets : pandas.core.frame.DataFrame
        ADCP time offsets.
    """
    # There are two files with time drift information, I must have done this at
    # sea and then on shore again. The second file does not have the instrument
    # type info which makes it easier to read as it is the same format as the
    # time drift file that is used for the SBE37.
    params = read_params()
    NISKINe_data = Path(params["path"])
    offset_file = NISKINe_data.joinpath("ADCP_time_offsets2.txt")
    time_offsets = pd.read_csv(
        offset_file,
        engine="python",
        header=0,
        delim_whitespace=True,
        parse_dates={"utc": [3, 4], "inst": [1, 2]},
        index_col="SN",
    )
    return time_offsets


def mooring_lonlat(mooring):
    """Read mooring position from nc file.

    Parameters
    ----------
    mooring : str
        Mooring ID

    Returns
    -------
    lon : float
        Longitude
    lat : float
        Latitude
    """

    params = read_params()
    NISKINe_data = Path(params["path"])
    # Mooring locations
    mooring_positions = xr.open_dataset(
        NISKINe_data.joinpath("niskine_mooring_locations.nc")
    )
    mooring_int = int(mooring[1])
    lon = mooring_positions.sel(mooring=mooring_int).lon_actual.data
    lat = mooring_positions.sel(mooring=mooring_int).lat_actual.data
    return lon, lat


def convert_time_stamp(time_np64):
    """Convert numpy datetime64 to tuple with year, month, day, hour, minute, second.

    Parameters
    ----------
    time_np64 : np.datetime64
        Time stamp

    Returns
    -------
    tuple
        Tuple with year, month, day, hour, minute, second
    """

    # need time stamps in the following format:
    # end_pc   = (2020, 10,  9, 20, 26,  0)
    dt = datetime.datetime.utcfromtimestamp(time_np64.tolist() / 1e9)
    return (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def load_default_parameters():
    editparams = dict(
        max_e=0.2,  # absolute max e
        max_e_deviation=2,  # max in terms of sigma
        min_correlation=64,  # 64 is RDI standard
    )

    tgridparams = dict(
        burst_average=True,
    )
    return editparams, tgridparams


def plot_raw_adcp(mooring, sn):
    """Plot raw ADCP time series and save figure as png.

    Parameters
    ----------
    mooring : str
        Mooring ID.
    sn : int
        ADCP serial number.
    """
    dir_data_raw, raw_files, dir_data_out, dir_fig_out = construct_adcp_paths(
        sn, mooring
    )
    raw_files_posix = gadcp.io.read_raw_rdi(
        [file.as_posix() for file in raw_files]
    )
    gadcp.adcp.plot_raw_adcp(raw_files_posix)
    name_plot_raw = dir_fig_out.joinpath(f"{mooring}_{sn}_raw")
    gv.plot.png(name_plot_raw)


def process_adcp(
    mooring,
    sn,
    dgridparams,
    ibad=None,
    n_ensembles=None,
    pressure_scale_factor=1,
):
    """Process ADCP data and save to netcdf file.

    Parameters
    ----------
    mooring : str
        Mooring ID.
    sn : int
        ADCP serial number.
    dgridparams : dict
        Depth grid parameters with fields dbot, dtop, and d_interval.
    ibad : int or None, optional
        Bad beam to exclude (zero-based). Defaults to None.
    n_ensembles : int or None, optional
        Process only the first n_ensembles. Defaults to None (process all ensembles).
    pressure_scale_factor : float, opional
        Factor for scaling the pressure time series.
    """

    dir_data_raw, raw_files, dir_data_out, dir_fig_out = construct_adcp_paths(
        sn, mooring
    )
    raw_files_posix = [file.as_posix() for file in raw_files]
    time_offsets = read_time_offsets()
    insttime = time_offsets.loc[sn].inst.to_datetime64()
    end_adcp = convert_time_stamp(insttime)
    utctime = time_offsets.loc[sn].utc.to_datetime64()
    end_pc = convert_time_stamp(utctime)

    lon, lat = mooring_lonlat(mooring)

    # process
    editparams, tgridparams = load_default_parameters()
    m, mcm, pa, data = gadcp.madcp.proc(
        raw_files_posix,
        lon,
        lat,
        editparams,
        tgridparams,
        dgridparams,
        end_pc,
        end_adcp,
        n_ensembles=n_ensembles,
        ibad=ibad,
        pressure_scale_factor=pressure_scale_factor,
    )

    # add metadata
    data.attrs["lon"] = lon
    data.attrs["lat"] = lat
    data.attrs["mooring"] = mooring
    data.attrs["sn"] = sn
    data.attrs["proc time"] = np.datetime64('now').astype('str')
    params = read_params()
    data.attrs["project"] = params["project"]

    # save netcdf
    name_data_proc = dir_data_out.joinpath(f"{mooring}_{sn}.nc")
    data.to_netcdf(name_data_proc)


def load_proc_adcp(mooring, sn):
    """Load processed ADCP data (netcdf file).

    Parameters
    ----------
    mooring : str
        Mooring ID.
    sn : int
        ADCP serial number.

    Returns
    -------
    data : xarray.Dataset
        Data as read from processed netcdf file.
    """

    dir_data_raw, raw_files, dir_data_out, dir_fig_out = construct_adcp_paths(
        sn, mooring
    )
    name_data_proc = dir_data_out.joinpath(f"{mooring}_{sn}.nc")
    data = xr.open_dataset(name_data_proc)
    return data


def plot_adcp(mooring, sn):
    """Plot processed ADCP u and v time series.

    Parameters
    ----------
    mooring : str
        Mooring ID.
    sn : int
        ADCP serial number.

    Returns
    -------
    data : xarray.Dataset
        Data as read from processed netcdf file.
    """

    data = load_proc_adcp(mooring, sn)
    fig, ax = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(7.5, 5),
        constrained_layout=True,
        sharey=True,
        sharex=True,
    )
    data.u.plot(ax=ax[0])
    data.v.plot(ax=ax[1])
    ax[0].invert_yaxis()
    gv.plot.concise_date_all()
    [axi.set(xlabel="", ylabel="depth [m]") for axi in ax]
    plt.suptitle(f"{data.attrs['project']} {mooring} SN{sn}")
    name_plot = f"{mooring}_{sn}_uv"
    gv.plot.png(name_plot)
    return data
