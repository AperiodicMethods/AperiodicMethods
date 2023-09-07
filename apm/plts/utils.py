"""Utilities for plots."""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from neurodsp.plts.utils import savefig

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
    positions: 'tr' - 'top right', 'tl' - 'top left'
    """

    if not xtp:
        if position == 'tl':
            xtp, ytp = 0.05, 0.8755
        if position == 'tr':
            xtp, ytp = 0.775, 0.8755

    ax.text(xtp, ytp, text, transform=ax.transAxes)


def formr(r_val):
    """Format a string representation of a correlation r-value."""

    return 'r={:1.2f}'.format(r_val)


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


# NOTE: ADD TO NDSP?
def make_axes(n_rows, n_cols, figsize=None, row_size=4, col_size=3.6,
              wspace=None, hspace=None, title=None, **plt_kwargs):
    """Make a subplot with multiple axes.

    Parameters
    ----------
    n_rows, n_cols : int
        The number of rows and columns axes to create in the figure.
    figsize : tuple of float, optional
        Size to make the overall figure.
        If not given, is estimated from the number of axes.
    row_size, col_size : float, optional
        The size to use per row / column.
        Only used if `figsize` is None.
    wspace, hspace : float, optional
        Spacing parameters for between subplots.
        These get passed into `plt.subplots_adjust`.
    title : str, optional
        A title to add to the figure.
    **plt_kwargs
        Extra arguments to pass to `plt.subplots`.

    Returns
    -------
    axes : 1d array of AxesSubplot
        Collection of axes objects.
    """

    if not figsize:
        figsize = (n_cols * col_size, n_rows * row_size)

    title_kwargs = plt_kwargs.pop('title', None)

    _, axes = plt.subplots(n_rows, n_cols, figsize=figsize, **plt_kwargs)

    if wspace or hspace:
        plt.subplots_adjust(wspace=wspace, hspace=hspace)

    if title:
        plt.suptitle(title,
                     fontsize=title_kwargs.pop('title_fontsize', 24),
                     **title_kwargs)

    return axes
