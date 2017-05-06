"""The EEGDev data has multiple redundant copies.
After full backup, use this to remove superfluous files, specifically:
    - Eye Tracking Data
    - Preprocessed Data in mat format
    - Raw Data in Raw format
"""

import os
import shutil

DAT_DIR = '/Users/thomasdonoghue/Documents/Research/1-Projects/Slope/2-Data/EEGDev/Subjs/'

####################################################################################################
####################################################################################################

def main():

    subjs = os.listdir(DAT_DIR)

    for subj in subjs:

        # Remove eye-tracking data
        try:
            shutil.rmtree(os.path.join(DAT_DIR, subj, 'Eyetracking'))
        except:
            pass

        # Remove mat format preprocessed data
        try:
            shutil.rmtree(os.path.join(DAT_DIR, subj, 'EEG', 'preprocessed', 'mat_format'))
        except:
            pass

        # Remove raw data
        try:
            shutil.rmtree(os.path.join(DAT_DIR, subj, 'EEG', 'raw'))
        except:
            pass


if __name__ == "__main__":
    main()
