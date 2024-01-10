"""Sim results plot functions."""

import numpy as np
import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig

from apm.plts.base import plot_lines
from apm.plts.settings import AP_COLOR, CB_COLOR, CF_COLOR, PW_COLOR
from apm.sim.settings import EXPS, FREQS, POWERS

###################################################################################################
###################################################################################################

@savefig
def plot_sims(x_vals, y_vals, y_shades, xlabel=None, ylabel=None, color=None,
              ylim=None, title=None, expected=None, figsize=(6, 5)):
    """Plot simulation results across a single parameter."""

    _, ax = plt.subplots(figsize=figsize)

    plot_lines(x_vals, y_vals, y_shades, color=color)
    if expected:
        plot_lines(x_vals, expected, color='black', linestyle='--', ax=ax)

    plot_lines(title=title, xlabel=xlabel, ylabel=ylabel, ylim=ylim, ax=ax)


@savefig
def plot_ap_sims(sims_exp, sims_exp_var, sims_comb, sims_comb_var, ylabel=None,
                 ylim=None, expected=None, legend_loc=None, figsize=(6, 5)):
    """Plot simulation results across aperiodic parameters."""

    _, ax = plt.subplots(figsize=figsize)

    if expected is not None:
        plot_lines(np.abs(EXPS), expected, color='k', linestyle='--', label='Expected')

    plot_lines(np.abs(EXPS), sims_exp, sims_exp_var, color=AP_COLOR, label='Aperiodic', ax=ax)
    plot_lines(np.abs(EXPS), sims_comb, sims_comb_var, color=CB_COLOR, label='Combined', ax=ax)
    plot_lines(xlabel='Simulated Exponent', ylabel=ylabel, ylim=ylim, ax=ax)
    plt.legend(fontsize=14, loc=legend_loc)


@savefig
def plot_pe_sims(sims_freq, sims_freq_var, sims_pow, sims_pow_var, ylabel=None,
                 ylim=None, expected=None, legend_loc=None, figsize=(6, 5)):
    """Plot simulation results across periodic parameters."""

    _, ax = plt.subplots(figsize=figsize)

    plot_lines(FREQS, sims_freq, sims_freq_var,
               color=CF_COLOR, xlabel='Oscillation Frequency', ylabel=ylabel, ax=ax)

    ax2 = ax.twiny()
    plot_lines(POWERS, sims_pow, sims_pow_var,
               color=PW_COLOR, xlabel='Oscillation Power', ax=ax2)

    leg_lines = [ax.get_lines()[0], ax2.get_lines()[0]]
    leg_labels = ['Frequency', 'Power']

    if expected is not None:
        plot_lines(FREQS, expected, color='k', linestyle='--', ax=ax)
        leg_lines.append(ax.get_lines()[1])
        leg_labels.append('Expected')

    if ylim:
        plt.ylim(ylim)

    plt.legend(leg_lines, leg_labels, loc=legend_loc, fontsize=14)
