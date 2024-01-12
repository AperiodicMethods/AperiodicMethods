"""Data plots."""

import warnings

import matplotlib.pyplot as plt
from matplotlib import cm

from fooof.utils import trim_spectrum
from neurodsp.spectral import compute_spectrum
from neurodsp.plts import plot_time_series, plot_power_spectra
from neurodsp.plts.utils import savefig

from mne.viz import plot_topomap

# Import custom code
import sys; from pathlib import Path
sys.path.append(str(Path('..').resolve()))
from apm.plts.utils import make_axes

###################################################################################################
###################################################################################################

# NOTE: use from NDSP when merged in there
@savefig
def plot_timeseries_and_psd(times, sig, fs, **plt_kwargs):
    """Plot a timeseries with it's associated power spectrum."""

    fig = plt.figure(figsize=plt_kwargs.pop('figsize', None))
    ax1 = fig.add_axes([0.0, 0.6, 1.3, 0.5])
    ax2 = fig.add_axes([1.5, 0.6, 0.6, 0.5])

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        plot_time_series(times, sig, **plt_kwargs, ax=ax1)

        freqs, psd = trim_spectrum(*compute_spectrum(sig, fs, nperseg=500), [1, 75])
        plot_power_spectra(freqs, psd, ax=ax2)


@savefig
def plot_topo_row(results, measures, info):
    """Helper function to plot a row of topographies."""

    axes = make_axes(1, len(measures), figsize=(2.5 * len(measures), 3), wspace=0.55)
    for measure, ax in zip(measures, axes):
        ax.set_title(measure, fontdict={'fontsize' : 10})
        plot_topomap(results[measure], info, cmap=cm.viridis,
                     contours=0, size=2, axes=ax, show=False)
