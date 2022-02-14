ADCP
====

[2020-05-17] A short update: I incorporated the time/space averaging code in the `gadcp` module and modified it to allow for burst processing. This seems to be working. I still need to simplify the input parameters a little bit as laid out above. With this, the steps to work on today are
  x Simplify input parameters.
  x List all ADCPs and time drift information in a file (make this a yaml file that we can read automatically?).
  x Run processing on all ADCPs. Also generate a plot of the raw ADCP data for each instrument.
  x Add processing code to proc repository.
  x Make `gadcp` public and add to dependencies of the proc environment. Also, clean it up a little bit.
  x Add processed ADCP data to server.
  - Still need to add option for external pressure time series to process ADCPs without pressure record.
  - Update Makefile to include ADCP processing.

[2020-05-24] Ran into a few issues, one of them the wrong pressure record for SN13481. This is now fixed for the time being and I also sent an email to RDI to inquire about this.

[2020-06-08] Still working out what exactly is going on with SN13481. I did solve an issue that I had with SN10219. The raw data files were split among two flash cards. I ended up combining the files using the Unix command `cat`.

[2022-02-10] Worked on masking bins for SN3109 that showed traces because of the top buoy giving reflections.

## magnetic declination
Magnetic declination at the mooring sites is -10.9. I still need to make sure that this is really applied when running the UH processing.

Magnetic declination as applied in the processing is -11.0. Close enough (the time stamp for the calculation might be slightly different than what I used above to run magdec in the shell). Now writing the magdec as used in the processing to the netcdf data structure.

## notes

### ADCP performance

The following is a list of ADCPs and how long they recorded data.
     
   SN  Mooring Performance
 3109  M1      Full record
 9408  M1      Full record
13481  M1      Full record; issues with pressure & rotation
14408  M1      Few days only
22476  M1      Few days only
 3110  M2      Full record
 8063  M2      No data
 8065  M2      Few days only. No pressure.
10219  M2      Full record
22479  M2      Few days only
23615  M2      Few days only
  344  M3      No data
 8122  M3      Few days only. No pressure.
12733  M3      Few days only
15339  M3      Few days only
15694  M3      Full record