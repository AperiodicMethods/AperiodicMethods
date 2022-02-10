"""Plots for the distributions of errors across methods."""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig

from .utils import get_ax

###################################################################################################
###################################################################################################

@savefig
def plot_boxplot_errors(errors, **plt_kwargs):
    """Plot a boxplot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    errors : dict
        Dictionary of errors per method.
    """

    ax = get_ax(None, figsize=plt_kwargs.pop('figsize', [10, 5]))

    ax.boxplot([errors[meth] for meth in errors.keys()],
                labels=errors.keys(), showfliers=False, **plt_kwargs);


@savefig
def plot_violin_errors(errors, ylim=None, **plt_kwargs):
    """Plot a violin plot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    errors : dict
        Dictionary of errors per method.
    """

    # Violin plot of the error distributions
    df = pd.DataFrame(errors)

    ax = get_ax(None, figsize=plt_kwargs.pop('figsize', [8, 2]))
    ax = sns.violinplot(data=df, cut=0, ax=ax, **plt_kwargs)

    ax.set_ylim(ylim)

    # Set font sizes
    ax.title.set_fontsize(32)
    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(18)

    plt.tight_layout()


@savefig
def plot_corr_matrix(corrs, **plt_kwargs):
    """Plot a correlation matrix, computed from the output of df.corr()."""

    mask = np.zeros_like(corrs, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    plt.figure(figsize=plt_kwargs.pop('figsize', [10, 8]))
    sns.heatmap(corrs, mask=mask, cmap='bwr',  vmin=-1, vmax=1, **plt_kwargs)
