"""Database related organization and utilities for slope fitting project."""

import os

########################################################################################
########################################################################################

class SLFDB(object):
    """Class to hold database information for slope fitting project.

    Attributes
    ----------
    project_path : str
        xx
    data_path : str
        xx
    subjs_path : str
        xx
    """

    def __init__(self, gen_paths=True):
        """Initialize SLFDB object."""

        # Set base path for project
        self.project_path = ("/Users/thomasdonoghue/Documents/"
                             "Research/1-Projects/Slope/")

        # Initialize paths
        self.data_path = str()
        self.subjs_path = str()
        self.psd_path = str()

        # Generate project paths
        if gen_paths:
            self.gen_paths()


    def gen_paths(self):
        """Generate paths."""

        self.data_path = os.path.join(self.project_path, '2-Data')
        self.subjs_path = os.path.join(self.data_path, 'EEGDev', 'Subjs')
        self.psd_path = os.path.join(self.data_path, 'psds')


    def check_subjs(self):
        """Check which subjects are avaiable in database."""

        # Check which subjects are available
        subjs = _clean_files(os.listdir(self.subjs_path))

        return subjs


    def get_subj_files(self, subj_number):
        """Get the preprocessed, EEG data file names (csv format) a specified subject."""

        dat_dir = os.path.join(self.subjs_path, subj_number,
                               'EEG', 'preprocessed', 'csv_format')

        files = os.listdir(dat_dir)

        eeg = [fi for fi in files if 'events' not in fi and 'channels' not in fi]
        evs = [fi for fi in files if 'events' in fi]
        chs = [fi for fi in files if 'channels' in fi]

        if not len(eeg) == len(evs) == len(chs):
            print('Oh Shit. Something seems to have gone wrong.')

        return eeg, evs, chs


    def get_psd_files(self):
        """Get the available PSD files."""

        psd_files = _clean_files(os.listdir(self.psd_path))

        return psd_files


    def gen_dat_path(self, subj_number, dat_file):
        """Generate full file path to a data file."""

        return os.path.join(self.subjs_path, subj_number,
                            'EEG', 'preprocessed', 'csv_format',
                            dat_file)

##
##

def _clean_files(files):
    """   """

    return list(filter(lambda x: x[0] != '.', files))
