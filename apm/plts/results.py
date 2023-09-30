"""Plots for the distributions of errors across methods."""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig
from neurodsp.plts.style import style_plot

from .utils import get_ax

###################################################################################################
###################################################################################################

@savefig
@style_plot
def plot_corr_matrix(corrs, **plt_kwargs):
    """Plot a correlation matrix, computed from the output of df.corr()."""

    # Create mask, only for non 1D data
    mask = None
    if 1 not in corrs.shape:
        mask = np.zeros_like(corrs, dtype=bool)
        mask[np.triu_indices_from(mask)] = True

    plt.figure(figsize=plt_kwargs.pop('figsize', None))
    sns.heatmap(corrs, mask=mask, cmap='bwr', vmin=-1, vmax=1, square=True,
                annot=plt_kwargs.pop('annot', True),
                fmt=plt_kwargs.pop('fmt', '1.2f'),
                cbar=plt_kwargs.pop('cbar', True),
                annot_kws={"size": 11},
                **plt_kwargs)
