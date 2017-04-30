"""Slope Fitting functions.

All these functions have the same design:
- They take freqs & psd IN LINEAR SPACE.
- They return a slope fit using a given method.
"""

import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import RANSACRegressor

import sys
sys.path.append('/Users/thomasdonoghue/Documents/GitCode/')
from foof.fit import FOOF

from utils import exclude_psd, CheckDims

################################################################################
################################################################################

@CheckDims
def fsl_ransac(freqs, psd):
    """Fit slope with RANSAC, across whole range."""""

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))
    sl_ran = ransac_model.estimator_.coef_[0][0]

    return sl_ran


@CheckDims
def fsl_ransac_alph(freqs, psd):
    """Fit slope with RANSAC, excluding pre-defined alpha band."""

    psd, freqs = exclude_psd(psd, freqs, [7, 14])

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))
    sl_ran_alph = ransac_model.estimator_.coef_[0][0]

    return sl_ran_alph


@CheckDims
def fsl_ransac_oscs(freqs, psd):
    """Fit slope with RANSAC, ignoring FOOF derived osc bands."""

    m = 2.0

    _, cens, _, bws = _foof_fit(freqs, psd)

    freqs, psd = _drop_oscs(freqs, psd, cens, bws)

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))
    sl_ran = ransac_model.estimator_.coef_[0][0]

    return sl_ran


@CheckDims
def fsl_rlm(freqs, psd):
    """Fit slope with RLM, across whole range."""

    fx = sm.add_constant(np.log10(freqs))

    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm = fit_rlm.params[1]

    return sl_rlm


@CheckDims
def fsl_rlm_alph(freqs, psd):
    """Fit slope with RLM, excluding pre-defined alpha band."""

    psd, freqs = exclude_psd(psd, freqs, [7, 14])

    fx = sm.add_constant(np.log10(freqs))

    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm_alph = fit_rlm.params[1]

    return sl_rlm_alph

@CheckDims
def fsl_rlm_oscs(freqs, psd):
    """Fit slope with RLM, ignoring FOOF derived osc bands."""

    chi, cens, pows, bws = _foof_fit(freqs, psd)

    freqs, psd = _drop_oscs(freqs, psd, cens, bws)

    fx = sm.add_constant(np.log10(freqs))
    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm = fit_rlm.params[1]

    return sl_rlm

################################################################################
################################################################################

def _foof_fit(freqs, psd):
    """Fit FOOF."""

    freqs = np.squeeze(freqs)

    foof = FOOF(min_p=0.2, res=np.mean(np.diff(freqs)),
                fmin=freqs.min(), fmax=freqs.max())
    foof.model(freqs, psd)

    return foof.chi_, foof.centers_, foof.powers_, foof.stdevs_

def _drop_oscs(freqs, psd, cens, bws):
    """Drop osc bands from PSD."""

    m = 2.0
    for cen, bw in zip(cens, bws):

        # Note: hack for old FOOF BW issue
        if bw > 3: continue

        psd, freqs = exclude_psd(psd, freqs, [cen-m*bw, cen+m*bw])

    return freqs, psd
