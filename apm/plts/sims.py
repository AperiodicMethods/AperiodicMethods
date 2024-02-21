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
def plot_sims(sim_vals, measures, xlabel=None, ylabel=None, color=None,
              expected=None, avg_func=np.mean, var_func=np.std,
              ylim=None, title=None, figsize=(6, 5)):
    """Plot simulation results across variations of a single parameter."""

    _, ax = plt.subplots(figsize=figsize)

    plot_lines(sim_vals, avg_func(measures, 1), var_func(measures, 1), color=color)
    if expected:
        plot_lines(sim_vals, expected, color='black', linestyle='--', ax=ax)

    plot_lines(title=title, xlabel=xlabel, ylabel=ylabel, ylim=ylim, ax=ax)


@savefig
def plot_ap_sims(sims_exp, sims_comb, measure=None, expected=None,
                 avg_func=np.mean, var_func=np.std, ylim=None,
                 legend_loc=None, figsize=(6, 5)):
    """Plot simulation results across aperiodic parameters."""

    _, ax = plt.subplots(figsize=figsize)

    if expected is not None:
        plot_lines(np.abs(EXPS), expected, color='k', linestyle='--', label='Expected')

    plot_lines(np.abs(EXPS), avg_func(sims_exp, 1), var_func(sims_exp, 1),
               color=AP_COLOR, label='Aperiodic', ax=ax)
    plot_lines(np.abs(EXPS), avg_func(sims_comb, 1), var_func(sims_comb, 1),
               color=CB_COLOR, label='Combined', ax=ax)
    plot_lines(xlabel='Simulated Exponent', ylabel=measure, ylim=ylim, ax=ax)
    plt.legend(fontsize=14, loc=legend_loc)


@savefig
def plot_pe_sims(sims_freq, sims_pow, measure=None, expected=None,
                 avg_func=np.mean, var_func=np.std,
                 ylim=None, legend_loc=None, figsize=(6, 5)):
    """Plot simulation results across periodic parameters."""

    _, ax = plt.subplots(figsize=figsize)

    plot_lines(FREQS, avg_func(sims_freq, 1), var_func(sims_freq, 1),
               color=CF_COLOR, xlabel='Oscillation Frequency', ylabel=measure, ax=ax)

    ax2 = ax.twiny()
    plot_lines(POWERS, avg_func(sims_pow, 1), var_func(sims_pow, 1),
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
