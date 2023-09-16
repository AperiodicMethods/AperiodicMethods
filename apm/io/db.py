"""Database related organization and utilities for aperiodic methods project."""

import os
from pathlib import Path

from apm.io.io import get_files

###################################################################################################
###################################################################################################

class APMDB():
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
        self.literature_path = self.data_path / 'literature'

        # ToDo: check if need to keep these:
        self.psds_path = self.data_path / 'psds'
        self.fooof_path = self.data_path / 'fooof'

        # Initialize paths if not already created
        self._mkpath(self.data_path)
        self._mkpath(self.figs_path)
        self._mkpath(self.sims_path)
        self._mkpath(self.literature_path)

        self._mkpath(self.fooof_path)
        self._mkpath(self.psds_path)


    def get_files(self, directory, **kwargs):
        """Get a list of available files in the specified directory.

        directory: {'data', 'figures', 'sims', 'psds', 'fooof', 'literature'}
        """

        return get_files(getattr(self, directory + '_path'), **kwargs)


    def make_fig_name(self, file_name, file_type='pdf'):
        """Return the file path for a figure with a given name."""

        return os.path.join(self.figs_path, file_name + '.' + file_type)


    def _mkpath(self, gen_path):
        """Create paths that don't exists."""

        if not os.path.isdir(gen_path):
            os.mkdir(gen_path)
