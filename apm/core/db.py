"""Database related organization and utilities for aperiodic methods project."""

import os

###################################################################################################
###################################################################################################

class APMDB(object):
    """Class to hold database information for aperiodic methods project.

    Attributes
    ----------
    project_path : str
        Base path for the project.
    data_path : str
        Path to all data.
    syns_path : str
    	Path to synthetic-fitting data.
    """

    def __init__(self, gen_paths=True):
        """Initialize APMDB object."""

        # Set base path for project
        self.project_path = ("/Users/tom/Documents/Research/1-Projects/1-Current/AperiodicMethods/")

        # Initialize paths
        self.data_path = str()
        self.syns_path = str()
        self.psd_path = str()
        self.fooof_path = str()

        # Generate project paths
        if gen_paths:
            self.gen_paths()


    def gen_paths(self):
        """Generate paths."""

        self.data_path = os.path.join(self.project_path, '2-Data')
        self.syns_path = os.path.join(self.data_path, 'syns')
        self.psd_path = os.path.join(self.data_path, 'psds')
        self.fooof_path = os.path.join(self.data_path, 'fooof')


    def check_files(self, file_type):
        """Check what files are available.

        file_type: {'syns', 'psd', 'fooof'}
        """

        return clean_files(os.listdir(getattr(self, file_type + '_path')))

    def get_files(self, file_type):
        """Get available files.

        file_type: {'syns', 'psd', 'fooof'}
        """

        return [fi.split('_')[0] for fi in self.check_files(file_type)]

###################################################################################################
###################################################################################################

def clean_files(files):
    """Clean a list of files, removing any hidden files."""

    return list(filter(lambda x: x[0] != '.', files))
