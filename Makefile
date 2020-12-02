# Makefile for NISKINe moored data processing
# NOTE: Needs GNU make version 4.3 or higher to work properly

# User name for the server is stored in credentials file that
# is included here. Change it to reflect your user name on kipapa.
# This file is excluded from being tracked in git by running
# `git update-index --assume-unchanged credentials.mk`
# on the command line. This can be undone with
# `git update-index --no-assume-unchanged credentials.mk`
include credentials.mk
# Server address
SERVER = kipapa.ucsd.edu
# Project base directory on server
KIPAPA_NISKINE = /Volumes/Ahua/data_archive/WaveChasers-DataArchive/NISKINE/
# Location of mooring data directory on the server. Note that we include a dot for
# replicating the directory structure when using rsync -R
REMOTE_DATA = $(USER)@$(SERVER):$(KIPAPA_NISKINE)./Moorings/NISKINE19/
# Local data directory. Using rsync, data will be copied here from the server with
# the path following the dot above (Moorings/NISKINE19)
LOCAL_DATA = /Users/gunnar/Projects/niskine/data/
PROC_DIR = /Users/gunnar/Projects/niskine/proc/

# determine current path # <- not sure if we need this anymore
ROOT_DIR=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# HELP {{{
# By default display the help listing below. Note: First target is always the
# default target, that's why help is displayed when just typing `make` without 
# providing a target. All comments starting with a second # will be included in
# the help listing.

## help              : Show this help section
.PHONY : help
help : Makefile
	@echo "Please use \`make <target>' where <target> is one of"
	@sed -n 's/^##//p' $<
# }}}

# FETCH REMOTE DATA {{{

# Group some processing steps
## sync_raw_data     : Sync raw data from server
sync_raw_data : sync_raw_adcp_data sync_raw_rbr_data \
	            sync_raw_sbe37_data sync_raw_sbe56_data

# Define arguments for rsync. The include pattern for $(1) can be replaced
# using call, see below.
# See more on the rsync options here:
# https://stackoverflow.com/questions/52343299/rsync-include-only-directory-pattern
rsync_args = -avzR --exclude='.DS_Store' --include='*/' --include='*$(1)*/**' \
			 --exclude='*' --prune-empty-dirs 

##   sync_raw_adcp_data   : Sync ADCP data from server
sync_raw_adcp_data :
	rsync $(call rsync_args,ADCP) $(REMOTE_DATA) $(LOCAL_DATA)

##   sync_raw_rbr_data    : Sync RBR Solo data from server
sync_raw_rbr_data :
	rsync $(call rsync_args,RBRSolo) $(REMOTE_DATA) $(LOCAL_DATA)

##   sync_raw_sbe56_data  : Sync SBE56 data from server
sync_raw_sbe56_data :
	rsync $(call rsync_args,SBE56) $(REMOTE_DATA) $(LOCAL_DATA)

##   sync_raw_sbe37_data  : Sync SBE37 data from server
sync_raw_sbe37_data :
	rsync $(call rsync_args,SBE37) $(REMOTE_DATA) $(LOCAL_DATA)

# }}}

# PROCESS RBRSOLO DATA {{{
RBR_RAW_FILES := $(wildcard $(LOCAL_DATA)Moorings/NISKINE19/M1/RBRSolo/raw/*.rsk)
RBR_PROC_FILES = $(subst raw,proc,$(subst .rsk,.nc,$(RBR_RAW_FILES)))

## proc_rbr          : Process RBRSolo data
.PHONY : proc_rbr
proc_rbr : $(RBR_PROC_FILES)
$(RBR_PROC_FILES) &: $(PROC_DIR)rbr/niskine_rbr_proc.py $(RBR_RAW_FILES)
	@echo 'processing RBR Solo files'
	python $<

# }}}

# PROCESS SBE56 DATA {{{
SBE56_RAW_FILES := $(wildcard $(LOCAL_DATA)Moorings/NISKINE19/M1/SBE56/raw/csv/*.csv)
SBE56_PROC_FILES := $(subst raw/csv,proc,$(subst .csv,.nc,$(SBE56_RAW_FILES)))

## proc_sbe56        : Process SBE56 data
.PHONY: proc_sbe56
proc_sbe56 : $(SBE56_PROC_FILES)
$(SBE56_PROC_FILES) &: $(PROC_DIR)sbe56/niskine_sbe56_proc.py $(SBE56_RAW_FILES)
	@echo 'processing SBE 56 files'
	python $<

# }}}

# PROCESS SBE37 DATA {{{

## proc_sbe37        : Process SBE37 data
.PHONY: proc_sbe37
proc_sbe37 : $(PROC_DIR)sbe37/niskine_sbe37_proc.py
	@echo 'processing SBE 37 files'
	python $<

# }}}
