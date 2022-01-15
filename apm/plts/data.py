"""Data plots, including for simulated data."""

import warnings

import matplotlib.pyplot as plt

from fooof.utils import trim_spectrum
from neurodsp.spectral import compute_spectrum
from neurodsp.plts import plot_time_series, plot_power_spectra

###################################################################################################
###################################################################################################

def plot_timeseries_and_psd(times, sig, fs, plt_kwargs={}):
    """Plot a timeseries with it's associated power spectrum."""

    fig = plt.figure()
    ax1 = fig.add_axes([0.0, 0.6, 1.3, 0.5])
    ax2 = fig.add_axes([1.5, 0.6, 0.6, 0.5])

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        plot_time_series(times, sig, xlim=[0, 2], **plt_kwargs, ax=ax1)

        freqs, psd = trim_spectrum(*compute_spectrum(sig, fs, nperseg=500), [1, 75])
        plot_power_spectra(freqs, psd, ax=ax2)
