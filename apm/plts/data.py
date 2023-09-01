"""Data plots."""

import warnings

import matplotlib.pyplot as plt

from fooof.utils import trim_spectrum
from fooof.plts.spectra import plot_spectra
from neurodsp.spectral import compute_spectrum
from neurodsp.plts import plot_time_series, plot_power_spectra
from neurodsp.plts.utils import savefig

from apm.plts.settings import FIGSIZE2

###################################################################################################
###################################################################################################

@savefig
def plot_psds_two(freqs1, psd1, freqs2, psd2, **plt_kwargs):
    """Plot side-by-side power spectra."""

    fig, axes = plt.subplots(1, 2, figsize=plt_kwargs.pop('figsize', FIGSIZE2))

    plot_spectra(freqs1, psd1, ax=axes[0], **plt_kwargs)
    plot_spectra(freqs2, psd2, ax=axes[1], **plt_kwargs)

    for ax in axes: ax.grid(False)
    plt.subplots_adjust(wspace=0.3)


# NOTE: use from NDSP when merged in there
@savefig
def plot_timeseries_and_psd(times, sig, fs, **plt_kwargs):
    """Plot a timeseries with it's associated power spectrum."""

    fig = plt.figure(figsize=plt_kwargs.pop('figsize', None))
    ax1 = fig.add_axes([0.0, 0.6, 1.3, 0.5])
    ax2 = fig.add_axes([1.5, 0.6, 0.6, 0.5])

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        plot_time_series(times, sig, xlim=plt_kwargs.pop('xlim', [0, 2]),
                         **plt_kwargs, ax=ax1)

        freqs, psd = trim_spectrum(*compute_spectrum(sig, fs, nperseg=500), [1, 75])
        plot_power_spectra(freqs, psd, ax=ax2)
