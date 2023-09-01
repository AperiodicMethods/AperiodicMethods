"""Sim results plot functions."""

import matplotlib.pyplot as plt

from neurodsp.plts.utils import savefig

from apm.plts.base import plot_lines
from apm.plts.settings import AP_COL, COMB_COL, FREQ_COLOR, POW_COLOR
from apm.sim.settings import EXPS, FREQS, POWERS

###################################################################################################
###################################################################################################

@savefig
def plot_ap_sims(sims_exp, sims_exp_var, sims_comb, sims_comb_var, ylabel=None):
    """Plot simulations across aperiodic parameters."""

    _, ax = plt.subplots(figsize=(6, 5))
    plot_lines(EXPS, sims_exp, sims_exp_var, color=AP_COL, label='Aperiodic', ax=ax)
    plot_lines(EXPS, sims_comb, sims_comb_var, color=COMB_COL, label='Combined', ax=ax)
    plot_lines(xlabel='Aperiodic Exponent', ylabel=ylabel, ax=ax)
    plt.legend(fontsize=14)


@savefig
def plot_pe_sims(sims_freq, sims_freq_var, sims_pow, sims_pow_var, ylabel=None):
    """Plot simulations across periodic parameters."""

    _, ax = plt.subplots(figsize=(6, 5))
    plot_lines(FREQS, sims_freq, sims_freq_var,
               color=FREQ_COLOR, xlabel='Oscillation Frequency', ylabel=ylabel, ax=ax)
    ax2 = ax.twiny()
    plot_lines(POWERS, sims_pow, sims_pow_var,
               color=POW_COLOR, xlabel='Oscillation Power', ax=ax2)
    plt.legend([ax.get_lines()[0], ax2.get_lines()[0]],
               ['Frequency', 'Power'], loc=4, fontsize=14)