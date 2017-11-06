"""Selectively copy over MIPDB_EEG data."""

import os
import shutil

####################################################################################################
####################################################################################################

# Subjects with no data (info from README)
SKIP_SUBJS = ['A00052593', 'A00054122', 'A00055801', 'A00056158', 'A00056640', 'A00056990']

# Additional subjects missing EEG data (from PublicFile)
SKIP_SUBJS = SKIP_SUBJS + ['A00055923', 'A00057135']

SOURCE_PATH = '/Volumes/WINDATA/MIPDB_EEGDev/Subjs/'
DEST_PATH = '/Users/tom/Desktop/CMI_Data/Subjs/'

####################################################################################################
####################################################################################################

def main():

    subjs = clean_files(os.listdir(SOURCE_PATH))
    folder_names = ['EEG', 'preprocessed', 'csv_format']

    for subj in subjs:

        if subj in SKIP_SUBJS:
            continue

        print('Copying subject # ', subj)

        # Create the subject specific folder data directory
        fdir = DEST_PATH
        for fn in [subj] + folder_names:
            fdir = os.path.join(fdir, fn)
            if os.path.exists(fdir):
                continue
            os.mkdir(fdir)

        source_dir = os.path.join(SOURCE_PATH, subj, *folder_names)
        dest_dir = os.path.join(DEST_PATH, subj, *folder_names)

        dat_files = clean_files(os.listdir(source_dir))

        for df in dat_files:

            s_file = os.path.join(source_dir, df)
            d_file = os.path.join(dest_dir, df)

            # Skip file if it exists
            if os.path.exists(d_file):
                continue

            # Copy file over
            shutil.copy(s_file, d_file)

def clean_files(files):
    return [it for it in files if it[0] is not '.']

####################################################################################################
####################################################################################################

if __name__ == "__main__":
    main()
