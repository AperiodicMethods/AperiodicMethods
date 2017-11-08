# PSDSlopeFitting

This repository / project has two aims: 
- To test various PSD slope fitting procedures on synthetic datasets, to assesss which is the best approach
- To apply the best practice slope fitting the the MIPDB ChildMind database

Note: If cloned, using scripts / notebooks inside this repo assumes that the 'slf' directory has been added to PYTHONPATH.

## Dependencies

This project is written in Python3.6

Dependencies:
- numpy
- scipy
- pandas
- scikit-learn
- matplotlib
- FOOOF (https://github.com/voytekresearch/fooof)

## SLF

SLF is a custom module for slope fitting. At it's core, it contains fit.py, with a range of slope fitting functions. 
Currently, it is also intermixed with utilities for the Slope Fitting Project, including dealing with the MIPDB dataset.

## Data
- EEGDev Dataset
    - EEG Dataset across developmental ages: childhood -> adult
        - This data: http://fcon_1000.projects.nitrc.org/indi/cmi_eeg/eeg.html
- Synthetic PSD data
    - Generated using FOOF synthetic PSD functions

## Legend (Notebooks)
- 01-SlopeFitting
    - An overview of the candidate slope fitting methods
- 02-SyntheticFitting
    - Creating Synthetic PSD data, and testing slope fitting approaches on them.
- 03-CompareSyntheticFits
    - A comparison of the slope-fitting performance, across the synthetic PSDs
- 04-EEGDataProcessing
    - Processing pipeline for the MIPDB EEG dataset, calculating PSDs, and fitting PSD slope
- 05-EEGDataGroupAnalysis
    - Analysis of the group level results of the MIPDB dataset.
    
Note: the above mentioned notebooks law out the pipelines used in this project. For actually running group level analysis, there are standalone python scripts. 

## Legend (Scripts)
- run_syn_fits.py
    - Generates synthetic data, and tests slope fitting methods upon them.
- proc_dev_dat.py
    - Script to process all of the EEGDev dataset.
