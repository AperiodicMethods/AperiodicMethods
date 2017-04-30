"""Slope Fitting functions."""

import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import RANSACRegressor

import sys
sys.path.append('/Users/thomasdonoghue/Documents/GitCode/')
from foof.fit import FOOF

from utils import exclude_psd, _check

################################################################################
################################################################################

def fsl_ransac(freqs, psd):
    """   """""

    freqs = _check(freqs)
    psd = _check(psd)

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))
    sl_ran = ransac_model.estimator_.coef_[0][0]

    return sl_ran


def fsl_ransac_alph(freqs, psd):
    """   """

    freqs = _check(freqs)
    psd = _check(psd)

    psd, freqs = exclude_psd(psd, freqs, [7, 14])

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))
    sl_ran_alph = ransac_model.estimator_.coef_[0][0]

    return sl_ran_alph


def fsl_ransac_oscs(freqs, psd):
    """   """

    psd = _check(psd)
    freqs = _check(freqs)

    m = 2.0

    _, cens, _, bws = _foof_fit(freqs, psd)

    for cen, bw in zip(cens, bws):
        psd, freqs = exclude_psd(psd, freqs, [cen-m*bw, cen+m*bw])

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))
    sl_ran = ransac_model.estimator_.coef_[0][0]

    return sl_ran


def fsl_rlm(freqs, psd):
    """   """

    freqs = _check(freqs)
    psd = _check(psd)

    fx = sm.add_constant(np.log10(freqs))

    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm = fit_rlm.params[1]

    return sl_rlm


def fsl_rlm_alph(freqs, psd):
    """   """

    freqs = _check(freqs)
    psd = _check(psd)

    psd, freqs = exclude_psd(psd, freqs, [7, 14])

    fx = sm.add_constant(np.log10(freqs))

    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm_alph = fit_rlm.params[1]

    return sl_rlm_alph


def fsl_rlm_oscs(freqs, psd):
    """   """

    psd = _check(psd)
    freqs = _check(freqs)

    chi, cens, pows, bws = _foof_fit(freqs, psd)

    m = 2.0
    for cen, bw in zip(cens, bws):
        # Note: hack for old FOOF BW issue
        if bw > 3: continue
        print(cen, bw)
        psd, freqs = exclude_psd(psd, freqs, [cen-m*bw, cen+m*bw])

    fx = sm.add_constant(np.log10(freqs))
    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm = fit_rlm.params[1]

    return sl_rlm

################################################################################
################################################################################

def _foof_fit(freqs, psd):
    """   """

    freqs = np.squeeze(freqs)

    foof = FOOF(min_p=0.2, res=np.mean(np.diff(freqs)),
                fmin=freqs.min(), fmax=freqs.max())
    foof.model(freqs, psd)

    return foof.chi_, foof.centers_, foof.powers_, foof.stdevs_
