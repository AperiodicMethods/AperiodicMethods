# SlopeFitOscs
Testing Slope Fitting approaches on synthetic PSDs, and applying these methods to EEG datasets.
In particular: what is the best fitting approach to use, and how can we best reduce oscillatory influences when estimating 1/f.

Note: If cloned, using scripts / notebooks inside this repo assumes that the directory has been added to PYTHONPATH.

## SLF
SLF is a custom module for slope fitting. At it's core, it contains fit.py, with a range of slope fitting functions. 
Currently, it is also intermixed with utilities for the Slope Fitting Project, including dealing with the EEGDev dataset.

## Data
- EEGDev Dataset
    - EEG Dataset across developmental ages: childhood -> adult
        - This data: http://fcon_1000.projects.nitrc.org/indi/cmi_eeg/eeg.html
- EEGChi Dataset
    - Example EEG data from Chicago group (courtesy of Jorge Yanar)
- Synthetic PSD data
    - Generated using FOOF synthetic PSD functions

## Legend (Notebooks)
- 01-SlopeFitting
    - Overview of the fitting methods, demonstrating them on real data (EEGChi data)
- 02-SynFits
    - Creating Synthetic PSD data, and testing slope fitting approaches on them.
- 03-Dev_DataOutline
    - Outline of EEGDev dataset, exploring the database.
- 04-Dev_DataProcessing
    - Processing EEGDev dataset, calculating PSDs.
- 05-Dev_SlopeFittign
    - Slope fitting PSDs from the EEGDev dataset.
    
## Legend (Scripts)
- proc_dev_dat.py
    - Script to process all of the EEGDev dataset.
- rm_ext_dat.py
    - Database management for EEGDev dataset, removing redundant data copies. 

## Notes
- These notebooks use different versions of Python, because otherwise everything would be too easy....
    - Notebooks running FOOF use py27
    - Notebooks running MNE use py36
