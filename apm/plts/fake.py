"""Plots for the distributions of errors from spectrum fitting methods."""

import pandas as pd
import matplotlib.pyplot as plt

###################################################################################################
###################################################################################################

def boxplot_errors(err_dists):
    """Plot a boxplot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    err_dists : dict
        Dictionary of error distributions, from SynFits object.
    """

    fig = plt.figure(figsize=[10, 5])
    plt.boxplot([err_dists[meth] for meth in err_dists.keys()],
                    labels=err_dists.keys(),
                    showfliers=False);


def violin_errors(err_dists):
    """Plot a violin plot of distributions of errors for each spectrum fit method.

    Parameters
    ----------
    err_dists : dict
        Dictionary of error distributions, from SynFits object.
    """

    import seaborn as sns

    # Violin plot of the error distributions
    df = pd.DataFrame(err_dists)
    plt.figure(figsize=[16, 6])
    ax = sns.violinplot(data=df, cut=0)
    plt.title('Error Distributions Across Spectrum Fitting Methods')

    # Restrict y-limits
    plt.ylim([-0.25, 8.5]);

    # Set font sizes
    ax.title.set_fontsize(32)
    for item in (ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(18)

    return ax

####################################################################################################
####################################################################################################

def _color_red_or_green(val):
    """Use colour code to visualize significant differences"""

    color = 'green' if val < 0.05 else 'red'
    return 'color: %s' % color
