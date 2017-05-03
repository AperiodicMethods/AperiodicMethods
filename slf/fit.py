"""Slope Fitting functions.

All these functions have the same design:
- They take freqs & psd IN LINEAR SPACE.
- They return a slope fit using a given method.
"""

import sys
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import RANSACRegressor

# Import FOOF - Set which version to import
#  NOTE: this is super messy / dangerous path usage - bad Tom.
#    (Also, this only works on Tom's laptop atm.)
#    The mess is to compare FOOF versions. Soon move to new FOOF only.

# Set which version of foof to use
FOOF_VER ='bayes'

if FOOF_VER == 'old':

    # Import FOOF (old version, in GitCode)
    sys.path.append('/Users/thomasdonoghue/Documents/GitCode')
    from foof.fit import FOOF

if FOOF_VER == 'bayes':

    # Import Bayes FOOF is currently on desktop to keep out of way of old FOOF
    sys.path.append('/Users/thomasdonoghue/Desktop/')
    from foof.fit import FOOF

from slf.core.utils import exclude_psd, CheckDims

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

def abs_err(val, fit):
    """Absolute error of fit."""

    return abs(val - fit)

def sqd_err(val, fit):
    """Squared error of fit."""

    return (val - fit)**2

################################################################################
################################################################################

def _foof_fit(freqs, psd):
    """Fit FOOF."""

    freqs = np.squeeze(freqs)

    if FOOF_VER == 'old':
        foof = FOOF(min_p=0.2, res=np.mean(np.diff(freqs)),
                    fmin=freqs.min(), fmax=freqs.max())
        foof.model(freqs, psd)

    if FOOF_VER == 'bayes':
        foof = FOOF(freqs, res=np.mean(np.diff(freqs)), min_p=0.2)
        foof.fit(psd)

    return foof.chi_, foof.centers_, foof.powers_, foof.stdevs_

def _drop_oscs(freqs, psd, cens, bws):
    """Drop osc bands from PSD."""

    m = 2.0
    for cen, bw in zip(cens, bws):

        # Note: hack for old FOOF BW issue
        if FOOF_VER == 'old':
            if bw > 3: continue

        psd, freqs = exclude_psd(psd, freqs, [cen-m*bw, cen+m*bw])

    return freqs, psd
