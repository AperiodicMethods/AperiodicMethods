"""Plots for the distributions of errors from spectrum fitting methods."""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

###################################################################################################
###################################################################################################

def boxplot_errors(err_dists):
    """Plot a boxplot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    err_dists : dict
        Dictionary of error distributions, from SimFits object.
    """

    fig = plt.figure(figsize=[10, 5])
    plt.boxplot([err_dists[meth] for meth in err_dists.keys()],
                labels=err_dists.keys(), showfliers=False);


def violin_errors(err_dists, ylim=None):
    """Plot a violin plot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    err_dists : dict
        Dictionary of error distributions, from SimFits object.
    """

    # Violin plot of the error distributions
    df = pd.DataFrame(err_dists)

    plt.figure(figsize=[8, 2])
    ax = sns.violinplot(data=df, cut=0)

    ax.set_ylim(ylim)

    # Set font sizes
    ax.title.set_fontsize(32)
    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(18)

    plt.tight_layout()
