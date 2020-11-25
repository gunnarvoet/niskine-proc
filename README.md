NISKINe Mooring Data Processing
===============================

### CTD
Need to process cast nearby M1.

### ADCP

### Flowquest

### SBE37
**12710, 12711 and 12712** stop sampling at their specified rate pre-maturely. Most likely due to drained batteries. They come back to sampling and all instruments have the recovery recorded, but there are jumps in the time series and the time series are too short. Need to cut them until the point where they first start to drop out. The clocks still seemed fine on recovery, scale the time offset to the good part of the time series.

Time of first battery failure now determined for each of these by comparison with **2864** on the same mooring.

**2864, 3638, 4922, 4923** worked fine.

### SBE56
Processing mostly done.
Some of the time series end early or have gaps. Not sure how to go about applying the time offset in these cases. Need to look into this. Looks like the instruments ran out of battery. Now terminating the time series where the first gaps start to show up.

### RBR
Processing mostly done.

**Issues:** No time offset for **72167**, **76611**. These instruments were downloaded on a computer that misbehaved.

Time offset for **72167** is determined by comparison with **72146** (located 10m below on the mooring). Comparing their time series while sitting in the lab after recovery shows a pretty reliable clock drift of 45s for this instrument. This time offset has been applied.

### Chipod
