"""Plot style related functions and utilities."""

import matplotlib.pyplot as plt

###################################################################################################
###################################################################################################

def custom_psd_style_no_grid(ax, **kwargs):

    ax.set_xticks([], minor=True)
    ax.set_yticks([], minor=True)

    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])

    plt.tight_layout()

def custom_psd_style_no_ticks(ax, **kwargs):

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
