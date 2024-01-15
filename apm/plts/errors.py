"""Plots for the distributions of errors across methods."""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig
from neurodsp.plts.style import style_plot

from .utils import get_ax

###################################################################################################
###################################################################################################

@savefig
@style_plot
def plot_boxplot_errors(errors, labels=None, **plt_kwargs):
    """Plot a boxplot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    errors : dict
        Dictionary of errors per method.
    """

    df = pd.DataFrame(errors)

    ax = get_ax(None, figsize=plt_kwargs.pop('figsize', [10, 5]))

    sns.boxplot(data=df, fliersize=0, ax=ax, **plt_kwargs)

    if labels:
        ax.set_xticklabels(labels)

    plt.tight_layout()


@savefig
@style_plot
def plot_violin_errors(errors, labels=None, **plt_kwargs):
    """Plot a violin plot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    errors : dict
        Dictionary of errors per method.
    """

    df = pd.DataFrame(errors)

    ax = get_ax(None, figsize=plt_kwargs.pop('figsize', [8, 2]))
    ax = sns.violinplot(data=df, cut=0, ax=ax, **plt_kwargs)

    if labels:
        ax.set_xticklabels(labels)

    ax.title.set_fontsize(32)
    for item in ax.get_xticklabels() + ax.get_yticklabels():
        item.set_fontsize(18)

    plt.tight_layout()
