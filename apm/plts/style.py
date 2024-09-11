"""Plot style related functions and utilities."""

import matplotlib.pyplot as plt

###################################################################################################
###################################################################################################

def custom_psd_style_no_grid(ax, **kwargs):
    """Custom styling for a power spectrum plot - no grid."""

    ax.set_xticks([], minor=True)
    ax.set_yticks([], minor=True)

    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])

    plt.tight_layout()

def custom_psd_style_no_ticks(ax, **kwargs):
    """Custom styling for a power spectrum plot - no ticks."""

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)

    if 'legend_loc' in kwargs:
        ax.legend(prop={'size': 20}, loc=kwargs['legend_loc'])

    ax.set_xlabel(ax.get_xlabel(), fontsize=24)
    ax.set_ylabel(ax.get_ylabel(), fontsize=24)

    plt.tight_layout()
