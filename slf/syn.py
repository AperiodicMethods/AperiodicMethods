"""

Code adapeted from original foof code, written by Erik Peterson.

"""

import numpy as np
import pandas as pd
import scipy.stats as stat

####################################################################################################
####################################################################################################

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

    for i in xrange(1, n):
        fs, spec = fn(**kwargs)
        X[:,i] = spec

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
