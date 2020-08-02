"""Plots for aperiodic methods project."""

import numpy as np
import matplotlib.pyplot as plt

from fooof.plts.spectra import (plot_spectrum, plot_spectra,
                                plot_spectrum_shading, plot_spectra_shading)

from apm.plts.utils import get_ax
from apm.plts.settings import FIGSIZE1, FIGSIZE2

###################################################################################################
###################################################################################################

def plot_psds(freqs, psds, log_freqs=False):
    """Plot one or many power spectra.

    Parameters
    ----------
    freqs : 1d array or list of 1d array
        Frequency values to plot, on the x-axis.
    psds : 1d array or list of 1d array
        Power values to plot, on the y-axis.
    log_freqs : bool, optional, default: False
        Whether to plot the frequency axis in log space.

    Notes
    -----
    This plots power values in log10 spacing.
    """

    ax = get_ax()

    if not isinstance(psds, list):
        plot_spectrum(freqs, psds, log_freqs=log_freqs, log_powers=True, ax=ax)
    else:
        plot_spectra(freqs, psds, log_freqs=log_freqs, log_powers=True, ax=ax)

    ax.grid(False)


def plot_psds_shades(freqs, psds, shades, log_freqs=False):
    """Plot one or many power spectra, with shades.

    Parameters
    ----------
    freqs : 1d array or list of 1d array
        Frequency values to plot, on the x-axis.
    psds : 1d array or list of 1d array
        Power values to plot, on the y-axis.
    shades : list of [float, float] or list of list of [float, float]
        Shaded region(s) to add to plot, defined as [lower_bound, upper_bound].
    log_freqs : bool, optional, default: False
        Whether to plot the frequency axis in log space.

    Notes
    -----
    This plots power values in log10 spacing.
    """

    ax = get_ax()

    if not isinstance(psds, list):
        plot_spectrum_shading(freqs, psds, shades, add_center=True,
                              log_freqs=log_freqs, log_powers=True, ax=ax)
    else:
        plot_spectra_shading(freqs, psds, shades, add_center=True,
                             log_freqs=log_freqs, log_powers=True, ax=ax)

    ax.grid(False)


def plot_psds_two(freqs1, psd1, freqs2, psd2):
    """Plot side-by-side power spectra."""

    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE2)

    plot_spectrum(freqs1, psd1, ax=axes[0])
    plot_spectrum(freqs2, psd2, ax=axes[1])

    for ax in axes: ax.grid(False)
    plt.subplots_adjust(wspace=0.3)
