"""Slope Fitting functions.

All these functions have the same design:
- They take freqs & psd IN LINEAR SPACE.
- They return a slope fit using a given method.
"""

import numpy as np
import statsmodels.api as sm
from scipy.optimize import curve_fit
from sklearn.linear_model import RANSACRegressor

from fooof import FOOOF
from fooof.funcs import loglorentzian_nk_function as expf

from slf.core.utils import exclude_psd, CheckDims1D, CheckDims2D

####################################################################################################
####################################################################################################

@CheckDims2D
def fsl_ols(freqs, psd):
    """Fit slope with OlS, across whole range."""

    fx = sm.add_constant(np.log10(freqs))

    ols_model = sm.OLS(np.log10(psd), fx).fit()
    sl_ols = ols_model.params[1]

    return sl_ols


@CheckDims2D
def fsl_ransac(freqs, psd):
    """Fit slope with RANSAC, across whole range."""

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))

    sl_ran = ransac_model.estimator_.coef_[0][0]

    return sl_ran


@CheckDims2D
def fsl_ransac_alph(freqs, psd):
    """Fit slope with RANSAC, excluding pre-defined alpha band."""

    freqs, psd = exclude_psd(freqs, psd, [7, 14])

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))
    sl_ran_alph = ransac_model.estimator_.coef_[0][0]

    return sl_ran_alph


@CheckDims2D
def fsl_ransac_oscs(freqs, psd):
    """Fit slope with RANSAC, ignoring FOOF derived osc bands."""

    _, cens, _, bws = _fooof_fit(freqs, psd)

    freqs, psd = _drop_oscs(freqs, psd, cens, bws)

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(psd))
    sl_ran = ransac_model.estimator_.coef_[0][0]

    return sl_ran


@CheckDims2D
def fsl_rlm(freqs, psd):
    """Fit slope with RLM, across whole range."""

    fx = sm.add_constant(np.log10(freqs))

    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm = fit_rlm.params[1]

    return sl_rlm


@CheckDims2D
def fsl_rlm_alph(freqs, psd):
    """Fit slope with RLM, excluding pre-defined alpha band."""

    freqs, psd = exclude_psd(freqs, psd, [7, 14])

    fx = sm.add_constant(np.log10(freqs))

    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm_alph = fit_rlm.params[1]

    return sl_rlm_alph


@CheckDims2D
def fsl_rlm_oscs(freqs, psd):
    """Fit slope with RLM, ignoring FOOF derived osc bands."""

    _, cens, _, bws = _fooof_fit(freqs, psd)

    freqs, psd = _drop_oscs(freqs, psd, cens, bws)

    fx = sm.add_constant(np.log10(freqs))
    fit_rlm = sm.RLM(np.log10(psd), fx).fit()
    sl_rlm = fit_rlm.params[1]

    return sl_rlm


@CheckDims1D
def fsl_exp(freqs, psd):
    """   """

    fit_exp, _ = curve_fit(expf, freqs, np.log10(psd), p0=[1, 1])
    sl_exp = -fit_exp[1]

    return sl_exp


@CheckDims1D
def fsl_exp_alph(freqs, psd):
    """   """

    freqs, psd = exclude_psd(freqs, psd, [7, 14], make_2D=False)

    fit_exp, _ = curve_fit(expf, freqs, np.log10(psd), p0=[1, 1])
    sl_exp_alph = -fit_exp[1]

    return sl_exp_alph


@CheckDims1D
def fsl_exp_oscs(freqs, psd):
    """   """

    _, cens, _, bws = _fooof_fit(freqs, psd)

    freqs, psd = _drop_oscs(freqs, psd, cens, bws)
    freqs = np.squeeze(freqs)
    psd = np.squeeze(psd)

    fit_exp, _ = curve_fit(expf, freqs, np.log10(psd), p0=[1, 1])
    sl_exp_excl = -fit_exp[1]

    return sl_exp_excl


@CheckDims1D
def fsl_fooof(freqs, psd):
    """   """

    f_res = _fooof_fit(freqs, psd)
    sl_fooof = -f_res[0]

    return sl_fooof


def abs_err(val, fit):
    """Absolute error of fit."""

    return abs(val - fit)


def sqd_err(val, fit):
    """Squared error of fit."""

    return (val - fit)**2

####################################################################################################
####################################################################################################

@CheckDims1D
def _fooof_fit(freqs, psd):
    """Fit FOOOF."""

    #
    fm = FOOOF(bandwidth_limits=[1, 8], verbose=False)
    fm.fit(freqs, psd, [freqs.min(), freqs.max()])

    #
    if len(fm._gaussian_params > 0):
        cens, pows, bws = fm._gaussian_params[:, 0], fm._gaussian_params[:, 1], fm._gaussian_params[:, 2]
    else:
        cens, pows, bws = np.array([]), np.array([]), np.array([])

    return fm.background_params_[1], cens, pows, bws


def _drop_oscs(freqs, psd, cens, bws):
    """Drop osc bands from PSD."""

    m = 2.0
    for cen, bw in zip(cens, bws):
        freqs, psd = exclude_psd(freqs, psd, [cen-m*bw, cen+m*bw])

    return freqs, psd
