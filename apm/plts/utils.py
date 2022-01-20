"""Utilities for plots."""

import os

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from neurodsp.plts.utils import savefig

from apm.core.db import APMDB
from apm.plts.settings import SAVE_EXT, FIGSIZE1

###################################################################################################
###################################################################################################

def get_ax(ax):
    """Check an axis object, define if null, and get current if None."""

    if not ax:
        if figsize is not None:
            _, ax = plt.subplots(figsize=figsize)
        else:
            ax = plt.gca()

    return ax


def truncate_colormap(cmap, minval=0.0, maxval=1.0):
    """Truncate a colormap range.

    Code adapted from:
    https://stackoverflow.com/questions/40929467/how-to-use-and-plot-only-a-part-of-a-colorbar-in-matplotlib
    """

    new_cmap = mcolors.LinearSegmentedColormap.from_list(
         'trunc({name},{a:.2f},{b:.2f})'.format(name=cmap.name, a=minval, b=maxval),
         cmap(np.linspace(minval, maxval, cmap.N)))

    return new_cmap


def color_red_or_green(value, threshold=0.001):
    """Use colour code to visualize significant differences."""

    color = 'green' if value < threshold else 'red'
    return 'color: %s' % color


@savefig
def plot_colorbar(cmap, vmin, vmax, label, figsize=(2, 6), orientation='vertical'):
    """Create a colorbar."""

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    fig, ax = plt.subplots(figsize=figsize)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation=orientation)

    cbar.set_label(label, fontsize=30)
    cbar.ax.tick_params(labelsize=20)

    fig.subplots_adjust(bottom=0.5)
    fig.subplots_adjust(right=0.45)

    plt.tight_layout()
