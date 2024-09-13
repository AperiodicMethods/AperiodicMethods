"""Utilities for plots."""

from functools import partial

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm

from neurodsp.plts.utils import savefig

from apm.plts.settings import EXT

###################################################################################################
###################################################################################################

def get_ax(ax, figsize):
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


def add_text(text, position='tr', xtp=None, ytp=None, ax=None):
    """Add text to a plot.

    positions:
        'tr' : 'top right'
        'tl' : 'top left'
        'br' : 'bottom right'
        'bl' : 'bottom left'
    """

    if not xtp:
        assert position in ['tl', 'tr', 'bl', 'br'], 'Position input not understood.'
        if position == 'tl':
            xtp, ytp = 0.050, 0.8755
            ha = 'left'
        if position == 'tr':
            xtp, ytp = 0.950, 0.8755
            ha = 'right'
        if position == 'bl':
            xtp, ytp = 0.050, 0.0750
            ha = 'left'
        if position == 'br':
            xtp, ytp = 0.950, 0.0750
            ha = 'right'

    ax.text(xtp, ytp, text, transform=ax.transAxes, ha=ha)


def formr(r_val):
    """Format a string representation of a correlation r-value."""

    return 'r={:1.2f}'.format(r_val)


@savefig
def plot_colorbar(label, vmin, vmax, cmap=cm.viridis, orientation='vertical', figsize=(2, 6)):
    """Create a colorbar."""

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    fig, ax = plt.subplots(figsize=figsize)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation=orientation)

    cbar.set_label(label, fontsize=30)
    cbar.ax.tick_params(labelsize=20)

    fig.subplots_adjust(bottom=0.5)
    fig.subplots_adjust(right=0.45)

    plt.tight_layout()


def figsave_kwargs(file_name, file_path, save_fig, directory=False):
    """Helper function to organizing save-related figure kwargs."""

    save_kwargs = {
        'file_name' : file_name + EXT,
        'file_path' : file_path,
        'save_fig' : save_fig,
    }

    if directory:
        save_kwargs['directory'] = save_kwargs.pop('file_path')

    return save_kwargs


def figsaver(save_fig, file_path, directory=False):
    """Helper function for partializing `figsave_kwargs` to only take file name."""

    return partial(figsave_kwargs, file_path=file_path, save_fig=save_fig, directory=directory)
