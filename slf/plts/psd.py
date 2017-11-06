"""Plots for slope fitting project."""

import numpy as np
import matplotlib.pyplot as plt

####################################################################################################
####################################################################################################

def plt_psd_1(freqs, dat, log_f=True, log_p=True, label=None):
    """Plot a single PSD."""

    min_f = 2; max_f = 40
    min_p = 0.01; max_p = 400

    if log_f:
        freqs = np.log10(freqs)
        min_f = np.log10(min_f)
        max_f = np.log10(max_f)

    if log_p:
        dat = np.log10(dat)
        min_p = np.log10(min_p)
        max_p = np.log10(max_p)

    plt.plot(freqs, dat, lw=2)

    plt.xlim([min_f, max_f])
    plt.ylim([min_p, max_p])


def plt_psd_2(freqs_1, dat_1, freqs_2, dat_2, log_f=True, log_p=True):
    """Plot two PSD's together."""

    plt.figure()
    plt_psd_1(freqs_1, dat_1, log_f, log_p)
    plt_psd_1(freqs_2, dat_2, log_f, log_p)
