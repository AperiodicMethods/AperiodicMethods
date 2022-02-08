"""Plots for the distributions of errors across methods."""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig

###################################################################################################
###################################################################################################

@savefig
def boxplot_errors(errors, **plt_kwargs):
    """Plot a boxplot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    errors : dict
        Dictionary of errors per method.
    """

    fig = plt.figure(figsize=plt_kwargs.pop('figsize', [10, 5]))
    plt.boxplot([errors[meth] for meth in errors.keys()],
                labels=errors.keys(), showfliers=False, **plt_kwargs);


@savefig
def violin_errors(errors, ylim=None, **plt_kwargs):
    """Plot a violin plot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    errors : dict
        Dictionary of errors per method.
    """

    # Violin plot of the error distributions
    df = pd.DataFrame(errors)

    plt.figure(figsize=plt_kwargs.pop('figsize', [8, 2]))
    ax = sns.violinplot(data=df, cut=0, **plt_kwargs)

    ax.set_ylim(ylim)

    # Set font sizes
    ax.title.set_fontsize(32)
    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(18)

    plt.tight_layout()
