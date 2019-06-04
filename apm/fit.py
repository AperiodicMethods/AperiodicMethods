"""Aperiodic Methods: power spectrum fitting approaches.

All these functions have the same design:
- They take freqs & spectrum IN LINEAR SPACE
- They return a 1/f fit using a given method
"""

import numpy as np
import statsmodels.api as sm
from scipy.optimize import curve_fit
from sklearn.linear_model import RANSACRegressor

from fooof import FOOOF
from fooof.core.funcs import expo_nk_function as expf

from apm.utils import exclude_spectrum
from apm.core.utils import CheckDims1D, CheckDims2D

###################################################################################################
###################################################################################################

@CheckDims2D
def fit_ols(freqs, spectrum):
    """Fit spectrum with OlS, across whole range."""

    fx = sm.add_constant(np.log10(freqs))

    ols_model = sm.OLS(np.log10(spectrum), fx).fit()
    result = ols_model.params[1]

    return result


@CheckDims2D
def fit_ols_alph(freqs, spectrum):
    """Fit spectrum with OlS, excluding pre-defined alpha band."""

    freqs, spectrum = exclude_spectrum(freqs, spectrum, [7, 14])

    fx = sm.add_constant(np.log10(freqs))

    ols_model = sm.OLS(np.log10(spectrum), fx).fit()
    result = ols_model.params[1]

    return result


@CheckDims2D
def fit_ols_oscs(freqs, spectrum):
    """Fit spectrum with OlS, ignoring FOOOF derived oscillation bands."""

    _, cens, _, bws = _fooof_fit(freqs, spectrum)
    freqs, spectrum = _drop_oscs(freqs, spectrum, cens, bws)

    fx = sm.add_constant(np.log10(freqs))

    ols_model = sm.OLS(np.log10(spectrum), fx).fit()
    result = ols_model.params[1]

    return result


@CheckDims2D
def fit_ransac(freqs, spectrum):
    """Fit spectrum with RANSAC, across whole range."""

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(spectrum))

    result = ransac_model.estimator_.coef_[0][0]

    return result


@CheckDims2D
def fit_ransac_alph(freqs, spectrum):
    """Fit spectrum with RANSAC, excluding pre-defined alpha band."""

    freqs, spectrum = exclude_spectrum(freqs, spectrum, [7, 14])

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(spectrum))
    result = ransac_model.estimator_.coef_[0][0]

    return result


@CheckDims2D
def fit_ransac_oscs(freqs, spectrum):
    """Fit spectrum with RANSAC, ignoring FOOOF derived oscillation bands."""

    _, cens, _, bws = _fooof_fit(freqs, spectrum)
    freqs, spectrum = _drop_oscs(freqs, spectrum, cens, bws)

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(spectrum))
    result = ransac_model.estimator_.coef_[0][0]

    return result


@CheckDims2D
def fit_rlm(freqs, spectrum):
    """Fit spectrum with RLM, across whole range."""

    fx = sm.add_constant(np.log10(freqs))

    fit_rlm = sm.RLM(np.log10(spectrum), fx).fit()
    result = fit_rlm.params[1]

    return result


@CheckDims2D
def fit_rlm_alph(freqs, spectrum):
    """Fit spectrum with RLM, excluding pre-defined alpha band."""

    freqs, spectrum = exclude_spectrum(freqs, spectrum, [7, 14])

    fx = sm.add_constant(np.log10(freqs))

    fit_rlm = sm.RLM(np.log10(spectrum), fx).fit()
    result = fit_rlm.params[1]

    return result


@CheckDims2D
def fit_rlm_oscs(freqs, spectrum):
    """Fit spectrum with RLM, ignoring FOOOF derived oscillation bands."""

    _, cens, _, bws = _fooof_fit(freqs, spectrum)
    freqs, spectrum = _drop_oscs(freqs, spectrum, cens, bws)

    fx = sm.add_constant(np.log10(freqs))
    fit_rlm = sm.RLM(np.log10(spectrum), fx).fit()
    result = fit_rlm.params[1]

    return result


@CheckDims1D
def fit_exp(freqs, spectrum):
    """Fit spectrum with an exponential fit."""

    fit_exp, _ = curve_fit(expf, freqs, np.log10(spectrum), p0=[1, 1])
    result = -fit_exp[1]

    return result


@CheckDims1D
def fit_exp_alph(freqs, spectrum):
    """Fit spectrum with an exponential fit, excluding pre-defined alpha band."""

    freqs, spectrum = exclude_spectrum(freqs, spectrum, [7, 14], make_2D=False)

    fit_exp, _ = curve_fit(expf, freqs, np.log10(spectrum), p0=[1, 1])
    result = -fit_exp[1]

    return result


@CheckDims1D
def fit_exp_oscs(freqs, spectrum):
    """Fit spectrum with an exponential fit, ignoring FOOOF derived oscillation bands."""

    _, cens, _, bws = _fooof_fit(freqs, spectrum)

    freqs, spectrum = _drop_oscs(freqs, spectrum, cens, bws)
    freqs = np.squeeze(freqs)
    spectrum = np.squeeze(spectrum)

    fit_exp, _ = curve_fit(expf, freqs, np.log10(spectrum), p0=[1, 1])
    result = -fit_exp[1]

    return result


@CheckDims1D
def fit_fooof(freqs, spectrum):
    """Fit FOOOF."""

    f_res = _fooof_fit(freqs, spectrum)
    result = -f_res[0]

    return result

###################################################################################################
###################################################################################################

@CheckDims1D
def _fooof_fit(freqs, spectrum):
    """Fit FOOOF."""

    fm = FOOOF(peak_width_limits=[1, 8], verbose=False)
    fm.fit(freqs, spectrum, [freqs.min(), freqs.max()])

    if len(fm.gaussian_params_ > 0):
        cfs, pws, bws = fm.gaussian_params_[:, 0], fm.gaussian_params_[:, 1], fm.gaussian_params_[:, 2]
    else:
        cfs, pws, bws = np.array([]), np.array([]), np.array([])

    return fm.aperiodic_params_[1], cfs, pws, bws


def _drop_oscs(freqs, spectrum, cfs, bws):
    """Drop osc bands from spectrum."""

    m = 2.0
    for cf, bw in zip(cfs, bws):
        freqs, spectrum = exclude_spectrum(freqs, spectrum, [cf-m*bw, cf+m*bw])

    return freqs, spectrum
