NISKINe Mooring Data Processing
===============================

Python processing files were written in jupyter notebooks and converted to python scripts using [jupytext](https://jupytext.readthedocs.io/en/latest/). They can be converted back to jupyter notebooks.

### CTD
Need to process cast nearby M1.


### ADCP


### Flowquest


### SBE37
Processing mostly done.

**2864, 3638, 4922, 4923** worked fine.

**Issues:** **12710, 12711 and 12712** stop sampling at their specified rate pre-maturely. Most likely due to drained batteries. They come back to sampling and all instruments have the recovery recorded, but there are jumps in the time series and the time series are too short. Need to cut them until the point where they first start to drop out. The clocks still seemed fine on recovery, scale the time offset to the good part of the time series.

Time of first battery failure now determined for each of these by comparison with **2864** on the same mooring.


### SBE56
Processing mostly done.

Some of the time series end early or have gaps. Not sure how to go about applying the time offset in these cases. Need to look into this.


### RBR
Processing done.

**Issues:** No time offset for **72167**, **76611**. These instruments were downloaded on a computer that misbehaved. Wrong time offset for **72146**, also due to misbehaving computer. Unfortunately, these instruments were not in the included in the clock calibration (warm water dip).
Time offsets for all three instruments (72146: 12s, 72167: 0s, 76611: 10s) were determined by comparison with a few instruments below.


### Chipod
