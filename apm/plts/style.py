"""Plot style related functions and utilities."""

import matplotlib.pyplot as plt

###################################################################################################
###################################################################################################

def custom_psd_style(ax, **kwargs):
    """Define custom styling for the PSD plots."""

    ax.set_xticks([], minor=True)
    ax.set_yticks([], minor=True)

    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])

    plt.tight_layout()
