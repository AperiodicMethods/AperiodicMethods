"""Helper functions for processing EEG data."""

import numpy as np
from scipy.stats import pearsonr
from itertools import combinations, product

# Import FOOOF
from fooof import FOOOF

####################################################################################################
####################################################################################################

def fit_fooof_lst(freqs, psds):
    """

    Parameters
    ----------
    freqs : 1d array
        xx
    psds : 2d array
        xx

    Returns
    -------

    """

    f_range = [3, 35]
    fm = FOOOF(bandwidth_limits=[1, 8], max_n_oscs=6)

    out = []
    for psd in psds:
        fm.fit(freqs, psd, f_range)
        out.append(fm.get_params())

    return out


def fit_fooof_3d(freqs, psds):
    """

    Parameters
    ----------
    freqs : 1d array
        xx
    psds : 3d array
        xx

    Returns
    -------

    """

    n_eps, n_chs, n_psds = psds.shape

    out = []

    for ep_ind in range(n_eps):
        out.append(fit_fooof_lst(freqs, np.squeeze(psds[ep_ind, :, :])))

    return out


def get_slopes(lst):
    """Get slope values from FOOOF model parameters.

    Parameters
    ----------
    lst : list of tuples
        List of FOOOF model output parameters.

    Returns
    -------
    list of float
        Slope values.
    """

    return [dat.background_params[1] for dat in lst]


def comb_corrs(lst):
    """

    Parameters
    ----------
    lst : list
        xx

    Returns
    -------
    corrs : 1d array
        xx
    """

    corrs = []
    for ii, jj in combinations(lst, 2):
        corrs.append(pearsonr(ii, jj)[0])

    return corrs


def bet_corrs(lst1, lst2):
    """

    Parameters
    ----------
    lst1 : list
        xx
    lst2 : list
        xx

    Returns
    -------
    corrs : 1d array
        xx
    """

    corrs = []

    for ii, jj in product(lst1, lst2):
        corrs.append(pearsonr(ii, jj)[0])

    return corrs
