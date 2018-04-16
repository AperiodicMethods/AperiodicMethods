# PSDSlopeFitting

Goal(s):
- To test various PSD slope fitting procedures on synthetic datasets
- To determine, empirically, how methods relate to each other, and which is the most accurate

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

## Legend (Notebooks)
- 01-SlopeFitting
    - An overview of the candidate slope fitting methods
- 02-SyntheticFitting
    - Creating Synthetic PSD data, and testing slope fitting approaches on them.
- 03-CompareSyntheticFits
    - A comparison of the slope-fitting performance, across the synthetic PSDs
    
Note: the above mentioned notebooks law out the pipelines used in this project. For actually running group level analysis, there are standalone python scripts. 

## Legend (Scripts)

- run_syn_fits.py
    - Generates synthetic data, and tests slope fitting methods upon them.
