"""Plots for """

import matplotlib.pyplot as plt

from .utils import save_figure

import seaborn as sns
sns.set_context('talk')

###################################################################################################
###################################################################################################

def plot_lines(x_vals=None, y_vals=None, xlabel=None, ylabel=None, figsize=None, ax=None,
               save_fig=False, file_name=None, file_path=None, **plt_kwargs):
    """Plot line plot comparing estimates to ground truth."""

    if not ax:
        if figsize is not None:
            _, ax = plt.subplots(figsize=figsize)
        else:
            ax = plt.gca()

    # Set default line arguments
    if 'lw' not in plt_kwargs: plt_kwargs.update({'lw':  3.5})

    # Create the plot
    if x_vals is not None:
        ax.plot(x_vals, y_vals, **plt_kwargs)

    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)

    if ax.get_legend_handles_labels()[0]: plt.legend()

    save_figure(save_fig, file_name, file_path)
