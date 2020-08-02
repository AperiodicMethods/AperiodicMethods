"""Utilities for plots."""

import os

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from apm.core.db import APMDB
from apm.plts.settings import SAVE_EXT, FIGSIZE1

###################################################################################################
###################################################################################################

def plot_colorbar(cmap, vmin, vmax, label, figsize=(2, 6), orientation='vertical', show=True,
                  save_fig=False, file_name=None, file_path=None):
    """Create a colorbar."""

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    fig, ax = plt.subplots(figsize=figsize)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation=orientation)

    cbar.set_label(label, fontsize=30)
    cbar.ax.tick_params(labelsize=20)

    fig.subplots_adjust(bottom=0.5)
    fig.subplots_adjust(right=0.45)

    plt.tight_layout()
    save_figure(save_fig, file_name, file_path)

    if not show:
        plt.close()


def truncate_colormap(cmap, minval=0.0, maxval=1.0):
    """Truncate a colormap range.

    Code adapted from:
    https://stackoverflow.com/questions/40929467/how-to-use-and-plot-only-a-part-of-a-colorbar-in-matplotlib
    """

    new_cmap = mcolors.LinearSegmentedColormap.from_list(
         'trunc({name},{a:.2f},{b:.2f})'.format(name=cmap.name, a=minval, b=maxval),
         cmap(np.linspace(minval, maxval, cmap.N)))

    return new_cmap


def save_figure(save_fig, file_name, file_path):
    """Save out a figure."""

    if save_fig:
        plt.tight_layout()
        file_name = file_name + SAVE_EXT
        plt.savefig(os.path.join(APMDB().figs_path, file_path, file_name))


def get_ax():
    """Helper function to get an axis of a specific size for plotting."""

    return plt.subplots(figsize=FIGSIZE1)[1]


def color_red_or_green(val):
    """Use colour code to visualize significant differences."""

    color = 'green' if val < 0.001 else 'red'
    return 'color: %s' % color
