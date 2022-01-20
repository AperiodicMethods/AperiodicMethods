"""Plots for """

import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig

from scipy.stats import spearmanr

from .utils import get_ax, add_text, formr

import seaborn as sns
sns.set_context('talk')

###################################################################################################
###################################################################################################

@savefig
def plot_dots(x_vals=None, y_vals=None, xlabel=None, ylabel=None,
              add_corr=True, corr_func=spearmanr, tposition='tr',
              figsize=None, ax=None, **plt_kwargs):
    """Plot data as dots."""

    ax = get_ax(ax, figsize)

    # Create the plot
    if x_vals is not None:
        ax.plot(x_vals, y_vals, '.', **plt_kwargs)

    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)

    if ax.get_legend_handles_labels()[0]: plt.legend()

    if add_corr:
        r_val, p_val = corr_func(x_vals, y_vals)
        add_text(formr(r_val), position=tposition, ax=ax)


@savefig
def plot_lines(x_vals=None, y_vals=None, xlabel=None, ylabel=None,
               figsize=None, ax=None, **plt_kwargs):
    """Plot data as line(s)."""

    ax = get_ax(ax, figsize)

    # Set default line arguments
    if 'lw' not in plt_kwargs: plt_kwargs.update({'lw':  3.5})

    # Create the plot
    if x_vals is not None:
        ax.plot(x_vals, y_vals, **plt_kwargs)

    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)

    if ax.get_legend_handles_labels()[0]: plt.legend()
