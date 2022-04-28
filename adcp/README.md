ADCP
====

[2020-05-17] A short update: I incorporated the time/space averaging code in the `gadcp` module and modified it to allow for burst processing. This seems to be working. I still need to simplify the input parameters a little bit as laid out above. With this, the steps to work on today are
  - DONE: Simplify input parameters.
  - DONE: List all ADCPs and time drift information in a file (make this a yaml file that we can read automatically?).
  - DONE: Run processing on all ADCPs. Also generate a plot of the raw ADCP data for each instrument.
  - DONE: Add processing code to proc repository.
  - DONE: Make `gadcp` public and add to dependencies of the proc environment. Also, clean it up a little bit.
  - DONE: Add processed ADCP data to server.
  - DONE: Add option for external pressure time series to process ADCPs without pressure record.
  - DONE: Remove trace in SN3110 dataset (similar to SN3109).
  - Update Makefile to include ADCP processing.

[2020-05-24] Ran into a few issues, one of them the wrong pressure record for SN13481. This is now fixed for the time being and I also sent an email to RDI to inquire about this.

[2020-06-08] Still working out what exactly is going on with SN13481. I did solve an issue that I had with SN10219. The raw data files were split among two flash cards. I ended up combining the files using the Unix command `cat`.

[2022-02-10] Worked on masking bins for SN3109 that showed traces because of the top buoy giving reflections.

[2022-03-15] Changing the processing notebook to adapt to the refactored and improved `gadcp` package.

## magnetic declination
Magnetic declination as applied in the processing is about -11.0 which matches a manual run of magdec. Now writing the magdec as used in the processing to the netcdf data structure.
