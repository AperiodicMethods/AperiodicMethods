"""

Some code adapted from code written by Erik Peterson (https://github.com/parenthetical-e)
"""

import numpy as np
import pandas as pd
import scipy.stats as stat

from fooof.funcs import loglorentzian_function, loglorentzian_nk_function, gaussian_function

####################################################################################################
####################################################################################################

CEN_FREQS = np.load('freqs.npy')
PROBS = np.load('probs.npy')

####################################################################################################
####################################################################################################

def sim_psd(f_range, sl_val, osc_params, noi_lev, f_res=0.5):
    """Simulate a PSD. Outputs a PSD in linear space.

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
    bg = np.power(10, loglorentzian_nk_function(freqs, *[0, sl_val]))

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
    """Generate a plausbile oscillation distribution for synthetic a synthetic PSD.

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
    if not n_oscs:
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

####################################################################################################
####################################################################################################

### OLD - ERIK APPROACHES - OLD ####

def fonef(f=0, f_sig=1, k=0.1, A=1, chi=2, B=0, C=0, f0=1, fmax=40, noi=0, res=1):
    """Defines a PSD by k*N(f, f_sig) + A/(F^chi + C) + B

    Parameters
    ----------
    f : scalar
        Frequency of the oscillation bump
    f_sig : scalar
        Bandwidth of the oscillation
    k : scalar
        Heigth of the oscillation
    A : scalar
        The 'rate' term
    chi : scalar
        PSD slope
    B : scalar
        Adds a white noise across all frequencies
    C : scalar
        Creates a low frequency knee
    f0 : scalar
        Initial frequency in PSD range
    fmax : scalar
        Maximum frequency in PSD range
    res : scalar
        Sampling resolution of the PSD (Hz)
    """

    fs = np.arange(f0, fmax+1, step=res, dtype=np.float)

    # Create osc?
    if f > 0:
        osc = stat.norm.pdf(fs, loc=f, scale=f_sig)
        osc = osc / osc.max()
    else:
        osc = np.zeros_like(fs)

    # 1/F back bone
    spec = k*osc + (A * (1 / (fs**chi + C))) + B

    # add noise?
    if noi > 0:
        spec = 10 ** (
            np.log10(spec) + np.random.normal(0, noi, size=spec.shape[0])
        )

    return fs, spec


def mfonef(mf=None, mf_sig=None, mk=None, **kwargs):
    """Create a PSD with multiple oscillatory peaks, based on

    k*N(f, f_sig) + A/(F^chi + C) + B

    Note `kwargs` get passed to `fonef()`
    """

    if mf is None:
        mf = [6, 12, 30]
    if mf_sig is None:
        mf_sig = [1, 2, 3]
    if mk is None:
        mk = [0.1] * 3

    if len(mf) != len(mf_sig):
        raise ValueError("Length of `mf` and `mf_sig` must match")
    if len(mf_sig) != len(mk):
        raise ValueError("Length of `mf_sig` and `mk` must match")

    # Remove 'noi' kwarg, for use at the end.
    try:
        noiv = kwargs['noi']
        del kwargs['noi']
    except KeyError:
        noiv = 0

    # Creeate a background spectrum, one with no oscillation
    fs, background = fonef(**kwargs)

    # Add the first oscillation, initialzing
    _, spec = fonef(f=mf[0], f_sig=mf_sig[0], k=mk[0], **kwargs)

    # Add the remaining oscillations, removing the background
    # before each addition. This way power is constant
    # as the spectrums are summed.
    for f, f_sig, k in zip(mf[1:], mf_sig[1:], mk[1:]):
        _, osc = fonef(f=f, f_sig=f_sig, k=k, **kwargs)
        spec += (osc - background)

    # Now that we've built up the noise-free spec
    # add noise, if requested.
    if noiv > 0:
        _, noispec = fonef(noi=noiv, **kwargs)
        noispec -= background
        spec += noispec

    return fs, spec


def synthesize(n, fn=fonef, **kwargs):
    """Create `n` column PSD dataset.

    n : numeric
        Number of columns of data
    kwargs:
        Passed to `fonef()`
    """

    # Init
    fs, spec = fn(**kwargs)
    X = np.zeros((fs.shape[0], n))
    X[:,0] = spec

    for i in range(1, n):
        fs, spec = fn(**kwargs)
        X[:, i] = spec

    return fs, X


def save_syn_psds(name, fs, X):
    """   """

    df = pd.DataFrame(X)
    df['fs'] = fs
    df.to_csv(name, sep=',', header=True, index=False)


def load_syn_psds(name, f_min=3, f_max=100):
    """   """

    # Load as fs, X
    df = pd.read_csv(name)

    fs = df['fs']
    fs = np.asarray(fs)
    del df['fs']

    X = np.asarray(df)

    # Drop low F
    mask = fs > f_min
    fs = fs[mask]
    X = X[mask,]

    # Drop high F
    mask = fs < f_max
    fs = fs[mask]
    X = X[mask,]

    return fs, X
