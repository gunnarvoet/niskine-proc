NISKINe Mooring Data Processing
===============================

Python processing files were written in jupyter notebooks and converted to python scripts using [jupytext](https://jupytext.readthedocs.io/en/latest/). They can be converted back to jupyter notebooks.

A conda environment with all packages needed for running the python processing scripts can be created by running `conda env create -f environemnt.yml`. The environment will be called `niskine-proc`.

The `Makefile` bundles a number of data syncronization and processing steps. Note that you need GNU make version 4.3 or higher for this to work properly. On Macs, this can be installed via `brew install make` using homebrew. Type `make help` to see various options.

### CTD
Need to process cast nearby M1.


### ADCP


### Flowquest


### SBE37
Processing done.

Some of the processing code lives in https://github.com/gunnarvoet/sbemoored.

**2864, 3638, 4922, 4923** worked fine.

**Issues (solved):** **12710, 12711** and **12712** stop sampling at their specified rate pre-maturely. Most likely due to drained batteries - apparently the little tool Seabird provides for calculating instrument endurance isn't that good and one has to be more conservative. The instruments come back to sampling and all of them have data recorded during the time of mooring recovery, but there are gaps in the time series and the time stamps are wrong once data start to drop out. The time series are now cut short at the point where they first start to drop out. The following times for cutting the time series short were determined by comparison with **2864** on the same mooring:
| SN  | last good data |
|-----|----------------|
|12710|2020-02-09 21:00|
|12711|2020-03-17 12:00|
|12712|2020-01-16 23:15|

The clocks of the affected instruments still seemed fine on recovery, time offsets were scaled linearly to the good part of the time series.


### SBE56
Processing mostly done.

Some of the time series end early or have gaps. Not sure how to go about applying the time offset in these cases. Need to look into this.


### RBR
Processing done.

**Issues (solved):** No time offset for **72167**, **76611**. These instruments were downloaded on a computer that misbehaved. Wrong time offset for **72146**, also due to misbehaving computer. Unfortunately, these instruments were not in the included in the clock calibration (warm water dip).
Time offsets for all three instruments (72146: 12s, 72167: 0s, 76611: 10s) were determined by comparison with a few instruments below.


### Chipod
