# SlopeFitOscs
Testing Slope Fitting approaches on synthetic PSDs, and applying these methods to EEG datasets.
In particular: what is the best fitting approach to use, and how can we best reduce oscillatory influences when estimating 1/f.

## Data
- EEGDev Dataset
    - EEG Dataset across developmental ages: childhood -> adult
        - This data: http://fcon_1000.projects.nitrc.org/indi/cmi_eeg/eeg.html
- EEGChi Dataset
    - Example EEG data from Chicago group (courtesy of Jorge Yanar)
- Synthetic PSD data
    - Generated using FOOF synthetic PSD functions

## Legend (Notebooks)
- SlopeFittingOscs
    - Overview of the fitting methods, demonstrating them on real data (EEGChi data)
- DataOutline
    - Outline of EEGDev dataset, exploring the database.
- DevData
    - Processing EEGDev dataset, calculating PSDs.
- SynFits
    - Creating Synthetic PSD data, and testing slope fitting approaches on them.

## Notes
- These notebooks use different versions of Python, because otherwise everything would be too easy....
    - Notebooks running FOOF use py27
    - Notebooks running MNE use py36
