"""Code for synthesizing PSDs."""

import numpy as np
import pandas as pd
import scipy.stats as stat

from fooof.core.funcs import expo_function, expo_nk_function, gaussian_function

###################################################################################################
###################################################################################################

# CEN_FREQS = np.load('freqs.npy')
# PROBS = np.load('probs.npy')

###################################################################################################
###################################################################################################

def sim_psd(f_range, sl_val, osc_params, noi_lev, f_res=0.5):
    """Simulate a PSD. Outputs a PSD in linear space.

    NOTE: OLD / DEPRECATED (DON'T USE THIS ONE)
        THIS IS SUPER-CEDED BY SYNTH IN FOOOF
        POTENTIAL BENEFIT TO USE FROM HERE - USING A CALLABLE TO GET OSC-DEF.
        - THIS FUNCTION ALSO HAS AN ERROR IN ADDING OSCILLATIONS.

    Parameters
    ----------
    f_range : [float, float]
        Frequency range to simulate, as [f_low, f_high].
    sl_val : float
        Slope of the background of the generated PSD.
    osc_params : list of list of [float, float, float] or callable
        Oscillation definitions, as [center frequency, power, bandwidth].
    noi_lev : float
        Amount of noise to add to the PSD (typically between 0 - 0.5).
    f_res : float, optional
        Frequency resolution of PSD. Default: 0.5.

    Returns
    -------
    freqs : 1d array
        Frequency vector for PSD.
    psd : 1d array
        Power values for the PSD.
    """

    if callable(osc_params):
        osc_params = osc_params()

    # Unpack oscillation definition(s)
    if len(osc_params) > 0 and isinstance(osc_params[0], list):
        osc_params = [val for osc in osc_params for val in osc]

    # Generate frequency vector
    freqs = np.arange(f_range[0], f_range[1]+f_res, f_res)

    # Generate background process
    bg = np.power(10, expo_nk_function(freqs, *[0, sl_val]))

    # Generate oscillations, if specified
    if len(osc_params) > 0:
        oscs = gaussian_function(freqs, *osc_params)
    else:
        oscs = np.zeros(len(freqs))

    # Combine background and overlying oscillations
    psd = bg + oscs

    # Add noise (gaussian white noise, independent at each frequency)
    psd = np.power(10, (np.log10(psd) + np.random.normal(0, noi_lev, size=len(freqs))))

    # Alternate noise profile
    # Replace power values: chi2 value, centered on sim power, scaled by 'noise param' with var in chi
    #   This is the actual distribution of an fft window
    #bg_noisy = np.array([chi2.rvs(2, loc=0, scale=val) for val in bg])
    #psd = bg_noisy + oscs

    # No good noise simulation
    #noise = [norm.rvs(0, val) for val in bg]
    #psd = bg + oscs + noise

    return freqs, psd


def sim_n_psds(n_psds, f_range, sl_val, osc_params, noi_lev, f_res=0.5):
    """

    Parameters
    ----------

    Returns
    -------

    """

    freqs = np.arange(f_range[0], f_range[1]+f_res, f_res)
    n_freqs = len(freqs)

    # Pre-allocate a matrix to store PSDs
    psds = np.zeros(shape=[n_freqs, n_psds])

    #
    for i in range(n_psds):
        _, psds[:, i] = sim_psd(f_range, sl_val, osc_params, noi_lev, f_res)

    return freqs, psds


def gen_osc_def(n_oscs=None):
    """Generate a plausible oscillation distribution for a synthetic PSD.

    Parameters
    ----------
    n_oscs : int, optional
        Number of oscillations to generate. If None, picked at random. Default: None.

    Returns
    -------
    oscs : list of list of [float, float, float], or []
        Oscillation definitions.
    """

    #
    if n_oscs is None:
        n_oscs = np.random.choice([0, 1, 2], p=[1/3, 1/3, 1/3])

    # Initialize list of oscillation definitions
    oscs = []

    # Define the power and bandwidth possibilities and probabilities
    pow_opts = [0.05, 0.10, 0.15, 0.20]
    pow_probs = [0.25, 0.25, 0.25, 0.25]
    bw_opts = [1, 1.5, 2]
    bw_probs = [1/3, 1/3, 1/3]

    # Generate oscillation definitions
    for osc in range(n_oscs):

        cur_cen = np.random.choice(CEN_FREQS, p=PROBS)

        while _check_duplicate(cur_cen, [it[0] for it in oscs]):
            cur_cen = np.random.choice(CEN_FREQS, p=PROBS)

        cur_amp = np.random.choice(pow_opts, p=pow_probs)
        cur_bw = np.random.choice(bw_opts, p=bw_probs)

        oscs.append([cur_cen, cur_amp, cur_bw])

    return oscs


def _check_duplicate(cur_cen, all_cens, window=1):
    """Check if a candidate center frequency has already been chosen.

    Parameters
    ----------
    cur_cen : float
        xx
    all_cens : list of float
        xx
    window : int, optional
        xx

    Returns
    -------
    bool
        Whether the candidate center frequncy is already included.
    """

    if len(all_cens) == 0:
        return False
    for ch in range(cur_cen-window, cur_cen+window+1):
        if ch in all_cens:
            return True

    return False
