"""Plots for the distributions of errors across methods."""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig

###################################################################################################
###################################################################################################

@savefig
def boxplot_errors(errors):
    """Plot a boxplot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    errors : dict
        Dictionary of errors per method.
    """

    fig = plt.figure(figsize=[10, 5])
    plt.boxplot([errors[meth] for meth in errors.keys()],
                labels=errors.keys(), showfliers=False);


@savefig
def violin_errors(errors, ylim=None):
    """Plot a violin plot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    errors : dict
        Dictionary of errors per method.
    """

    # Violin plot of the error distributions
    df = pd.DataFrame(errors)

    plt.figure(figsize=[8, 2])
    ax = sns.violinplot(data=df, cut=0)

    ax.set_ylim(ylim)

    # Set font sizes
    ax.title.set_fontsize(32)
    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(18)

    plt.tight_layout()
