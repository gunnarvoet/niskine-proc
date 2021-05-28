NISKINe Mooring Data Processing
===============================

Python processing files were written in Jupyter notebooks and converted to python scripts using [jupytext](https://jupytext.readthedocs.io/en/latest/). They can be converted back to Jupyter notebooks.

A [conda](https://docs.conda.io/en/latest/) environment with all packages needed for running the python processing scripts can be created by running `conda env create -f environemnt.yml`. The newly created environment will be called `niskine-proc`.

The `Makefile` bundles a number of data synchronization and processing steps. Note that you need GNU make version 4.3 or higher for this to work properly. On Macs, this can be installed via `brew install make` using [homebrew](https://brew.sh/). Type `make help` to see various options for running the Makefile.

### CTD
Need to process cast nearby M1.


### ADCP


### Flowquest

Processing -> need to fix the conversion from Instrument velocities to Earth coordinates. AW is waiting for LinkQuest to write back with the correct conversion. 

Processing is to be run using matlab - Flowquest_text2mat_NISKINe.m to read in the fq_converted .DAT.txt files and generate the FQ structure which is saved in fq_converted/ called FQ_output.mat. 

Since the E4 header was missing in the binary and text files (header containing all earth coordinate data), the earth coordinate velocity needed to be calculated by hand using the instructions from LinkSys. Using the conversion in the file "Velocity relationship between instrument coordinate and earth coordinate1.pdf" and the matlab file - FQ_ConverInstrument2Earth in flowquest_mfiles/, a new output file with Earth coordinate velocity was added to FQ_output_Earth.mat. 

As a second check on the conversion to Earth coordinates, fq/flowquest_mfiles/FQ_ConverInstrument2Earth_TestPhilExData.m is used to compare with the PhilEx deployment that recorded in both instrument and Earth coordinates. 

The pressure record from the FQ was not looking realistic. Waiting for LinkQuest to determine the issue. Fro now, the long range ADCP isabove. the FQ is used to interpolate a realistic pressure (fq/flowquest_mfiles/FQ_interpolateNewPressure.m). 

Final output files: 
fq/fq_converted/FQ_output --> beam and instrument coordinates
fq/fq_converted/FQ_output_EarthCoords --> conversion to Earth coordinates as FQ.Earth.VN, .VE and .VW. Waiting for LinkQuest to update routines (not working yet)
fq/fq_converted/FQ_InterpolatedFinal.mat --> final output file to be used (!! FQ.Earth outputs are currently not correct)

Final figure: 
fig/M2_CurrentsFull.png made by fq/flowquest_mfiles/FQ_interpolateNewPressure.m

### SBE37
Processing done.

Some of the processing code lives in a separate repository at https://github.com/gunnarvoet/sbemoored.

**2864, 3638, 4922, 4923** worked fine.

**Issues (solved):** **12710, 12711** and **12712** stop sampling at their specified rate pre-maturely. Most likely due to drained batteries - apparently the little tool Seabird provides for calculating instrument endurance isn't that good and one has to be more conservative. The instruments come back to sampling and all of them have data recorded during the time of mooring recovery, but there are gaps in the time series and the time stamps are wrong once data start to drop out. The time series are now cut short at the point where they first start to drop out. The following times for cutting the time series short were determined by comparison with **2864** on the same mooring:
| SN  | last good data |
|-----|----------------|
|12710|2020-02-09 21:00|
|12711|2020-03-17 12:00|
|12712|2020-01-16 23:15|

The clocks of the affected instruments still seemed fine on recovery, time offsets were scaled linearly to the good part of the time series.


### SBE56
Processing done.

Some of the processing code lives in a separate repository at https://github.com/gunnarvoet/sbemoored.

Some of the time series have gaps. The time stamps seem OK. Re-downloading the data files from the affected instruments did not help. Seaterm shows a number of events recorded for the affected instruments, see example for **6435** below:

![SBE56 Seaterm Screenshot](fig/sbe56_seaterm_screenshot.png)

Clicking the events number brings up the following window:

![SBE56 Event Listing Screenshot](fig/sbe56_event_listing_screenshot.png)

Seems like there were power issues throughout the deployment that caused gaps in the time series.


### RBR
Processing done.

Some of the processing code lives in a separate repository at https://github.com/gunnarvoet/rbrmoored.


**Issues (solved):** No time offset for **72167**, **76611**. These instruments were downloaded on a computer that misbehaved. Wrong time offset for **72146**, also due to misbehaving computer. Unfortunately, these instruments were not in the included in the clock calibration (warm water dip).
Time offsets for all three instruments (72146: 12s, 72167: 0s, 76611: 10s) were determined by comparison with a few instruments below.


### Chipod
