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

        # Generate project paths
        if gen_paths:
            self.gen_paths()


    def gen_paths(self):
        """Generate paths."""

        # Level 1 paths
        self.data_path = self.base_path / 'data'
        self.figs_path = self.base_path / 'figures'

        # Data path subfolders
        self.sims_path = self.data_path / 'sims'
        self.psds_path = self.data_path / 'psds'
        self.fooof_path = self.data_path / 'fooof'
        self.literature_path = self.data_path / 'literature'

        # Initialize paths if not already created
        self._mkpath(self.data_path)
        self._mkpath(self.figs_path)
        self._mkpath(self.sims_path)
        self._mkpath(self.psds_path)
        self._mkpath(self.fooof_path)
        self._mkpath(self.literature_path)


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
