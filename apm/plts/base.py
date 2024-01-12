"""Base plot functions."""

import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig
from neurodsp.plts.style import style_plot

from scipy.stats import spearmanr

from .utils import get_ax, add_text, formr

###################################################################################################
###################################################################################################

@savefig
@style_plot
def plot_dots(x_vals=None, y_vals=None, add_corr=True, corr_func=spearmanr,
              tposition='tr', expected=None, ax=None, **plt_kwargs):
    """Plot data as dots."""

    ax = get_ax(ax, figsize=plt_kwargs.pop('figsize', None))

    if expected:
        ax.plot(expected, expected, color='black', linestyle='--', alpha=0.35)

    if x_vals is not None:
        ax.scatter(x_vals, y_vals, **plt_kwargs)

    if ax.get_legend_handles_labels()[0]:
        plt.legend()

    if add_corr:
        r_val, p_val = corr_func(x_vals, y_vals)
        add_text(formr(r_val), position=tposition, ax=ax)


@savefig
@style_plot
def plot_lines(x_vals=None, y_vals=None, shade_vals=None, ax=None, **plt_kwargs):
    """Plot data as line(s)."""

    ax = get_ax(ax, figsize=plt_kwargs.pop('figsize', None))

    if 'lw' not in plt_kwargs:
        plt_kwargs.update({'lw':  3.5})

    if x_vals is not None:
        ax.plot(x_vals, y_vals, **plt_kwargs)

    if shade_vals is not None:
        ax.fill_between(x_vals, y_vals-shade_vals, y_vals+shade_vals,
                        color=plt_kwargs.pop('color', None), alpha=0.2)

    if ax.get_legend_handles_labels()[0]:
        plt.legend()
