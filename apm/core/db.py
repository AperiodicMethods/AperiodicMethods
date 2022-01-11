"""Database related organization and utilities for aperiodic methods project."""

import os
from pathlib import Path

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
    sims_path : str
    	Path to simulated data.
    psds_path : str
        Path to power spectra.
    fooof_path : str
        Path to FOOOF files.
    """

    def __init__(self, base_path=None, gen_paths=True):
        """Initialize APMDB object."""

        if not base_path:
            base_path = Path(__file__).parents[2]

        # Set base path for project
        self.base_path = base_path

        # Initialize paths
        self.data_path = str()
        self.sims_path = str()
        self.psds_path = str()
        self.fooof_path = str()
        self.figs_path = str()

        # Generate project paths
        if gen_paths:
            self.gen_paths()

    def gen_paths(self):
        """Generate paths."""

        self.data_path = os.path.join(self.base_path, 'data')
        self.figs_path = os.path.join(self.base_path, 'figures')
        self.sims_path = os.path.join(self.data_path, 'sims')
        self.psds_path = os.path.join(self.data_path, 'psds')
        self.fooof_path = os.path.join(self.data_path, 'fooof')

        self._mkpath(self.data_path)
        self._mkpath(self.figs_path)
        self._mkpath(self.sims_path)
        self._mkpath(self.psds_path)
        self._mkpath(self.fooof_path)

    def check_files(self, file_type):
        """Check what files are available.

        file_type: {'sims', 'psd', 'fooof'}
        """

        return clean_files(os.listdir(getattr(self, file_type + '_path')))

    def get_files(self, file_type):
        """Get available files.

        file_type: {'sims', 'psd', 'fooof'}
        """

        return [fi.split('_')[0] for fi in self.check_files(file_type)]

    def make_fig_name(self, file_name, file_type='pdf'):
        """Return the file path for a figure with a given name."""

        return os.path.join(self.figs_path, file_name + '.' + file_type)

    def _mkpath(self, gen_path):
        """Created paths that don't exists."""

        if not os.path.isdir(gen_path):
            os.mkdir(gen_path)

###################################################################################################
###################################################################################################

def clean_files(files):
    """Clean a list of files, removing any hidden files."""

    return list(filter(lambda x: x[0] != '.', files))
