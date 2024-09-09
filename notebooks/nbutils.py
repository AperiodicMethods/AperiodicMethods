"""Utilities for working in Jupyter notebooks."""

import sys
import warnings
from pathlib import Path

import seaborn as sns

###################################################################################################
###################################################################################################

def setup_notebook(set_plt_context=True):
    """Setup notebook state."""

    # Add the local path up one directory to allow for importing local code
    sys.path.append(str(Path('..').resolve()))
    
    # Squash deprecation warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    # Set the plot context
    if set_plt_context:
        sns.set_context('talk')
