"""Database related organization and utilities for slope fitting project."""

import os

##
##

class SLFDB(object):
    """


    """

    def __init__(self, gen_paths=True):
        """   """

        # Set base path for project
        self.project_path = ("/Users/thomasdonoghue/Documents/"
                             "Research/1-Projects/Slope/")

        # Initialize paths
        self.data_path = str()
        self.subjs_path = str()

        #
        if gen_paths:
            self.gen_paths()


    def gen_paths(self):
        """   """

        self.data_path = os.path.join(self.project_path, '2-Data')
        self.subjs_path = os.path.join(self.data_path, 'EEGDev', 'Subjs')

    def check_subjs(self):
        """   """

        # Check what subjects are available
        subjs = os.listdir(self.subjs_path)
        subjs= list(filter(lambda x: x[0] != '.', subjs))

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
            print('Oh Shit. Something seems to have gong wrong.')

        return eeg, evs, chs
