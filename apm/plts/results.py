"""Plots for the distributions of errors across methods."""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm

from mne.viz import plot_topomap

from neurodsp.plts.utils import savefig

###################################################################################################
###################################################################################################

@savefig
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

    cax = plt.gca()
    if 1 in corrs.shape:
        cax.set_xticks([])
        cax.set_yticks([])
    else:
        cax.set_xticklabels(cax.get_xticklabels(), rotation=45, fontsize=10, ha='right')
        cax.set_yticklabels(cax.get_yticklabels(), rotation=0, fontsize=10)


@savefig
def plot_topo(data, info, size=2, **plt_kwargs):
    """Helper function for plotting topographies."""

    plot_topomap(data, info, cmap=cm.viridis, contours=0, size=size, show=False, **plt_kwargs)
