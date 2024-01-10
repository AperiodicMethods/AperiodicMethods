"""Aperiodic Methods: power spectrum fitting approaches.

All these functions have the same design:
- They take freqs & spectrum IN LINEAR SPACE
- They return a 1/f fit using a given method
"""

import warnings

import numpy as np
import statsmodels.api as sm
from scipy.stats import ranksums
from scipy.optimize import curve_fit
from sklearn.linear_model import RANSACRegressor

# Ignore deprecation / update warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from fooof import FOOOF
    from fooof.core.funcs import expo_nk_function as expf

from apm.analysis.error import abs_err
from apm.utils.data import exclude_spectrum
from apm.utils.decorators import CheckDims1D, CheckDims2D
from apm.methods.settings import ALPHA_RANGE

###################################################################################################
###################################################################################################

class SpectralFits():
    """Class object for fitting power spectra using multiple methods."""

    def __init__(self):
        """Initialize object."""

        self.fit_funcs = {'OLS' : fit_ols,
                          'OLS-EA' : fit_ols_alph,
                          'OLS-EO' : fit_ols_oscs,
                          'RLM' : fit_rlm,
                          'RLM-EA' : fit_rlm_alph,
                          'RLM-EO' : fit_rlm_oscs,
                          'RAN' : fit_ransac,
                          'RAN-EA' : fit_ransac_alph,
                          'RAN-EO' : fit_ransac_oscs,
                          'EXP' : fit_exp,
                          'EXP-EA' : fit_exp_alph,
                          'EXP-EO' : fit_exp_oscs,
                          'SPECPARAM' : fit_specparam}
        self.initialize_error_dict(0)


    def __add__(self, other):
        """Overload addition, to add errors fit across different datasets."""

        out = SpectralFits()

        for key, vals in other.errors.items():
            out.errors[key] = np.append(self.errors[key], other.errors[key])

        return out


    def __len__(self):
        """"Define length of the object as the number of computed errors."""

        return len(self.errors[self.labels[0]])


    @property
    def labels(self):
        """Labels for all the available fit functions."""

        return list(self.fit_funcs.keys())


    @property
    def n_methods(self):
        """The number of methods available in the object."""

        return len(self.labels)


    def initialize_error_dict(self, n_psds):
        """Create a dictionary to store fitting errors."""

        self.errors = dict()
        for key in self.labels:
            self.errors[key] = np.zeros(n_psds)


    def fit_spectra(self, exp, freqs, powers):
        """Fit spectra with available methods."""

        n_psds, _ = powers.shape
        self.initialize_error_dict(n_psds)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            for ki, fn in self.fit_funcs.items():
                for ind in range(n_psds):
                    try:
                        self.errors[ki][ind] = abs_err(-exp, fn(freqs, powers[ind, :]))
                    except:
                        self.errors[ki][ind] = np.nan


    def compare_errors(self):
        """Compare error distributions between methods."""

        comps = np.zeros([self.n_methods, self.n_methods])

        for ii, ki in enumerate(self.labels):
            for ij, kj in enumerate(self.labels):
                stat, p_val = ranksums(self.errors[ki], self.errors[kj])
                comps[ii, ij] = p_val

        return comps


    def compute_avg_errors(self, avg='median'):
        """Compute average errors per method."""

        avg_errors = []
        for key, vals in self.errors.items():
            if avg == 'median':
                avg_errors.append((np.nanmedian(vals), key))
            elif avg == 'mean':
                avg_errors.append((np.nanmean(vals), key))
            else:
                raise ValueError('Average type not understood')
        avg_errors.sort()

        return avg_errors


    def compute_std_errors(self):
        """Compute standard deviation of error per method."""

        std_errors = []
        for key, vals in self.errors.items():
            std_errors.append((np.nanstd(vals), key))
        std_errors.sort()

        return std_errors


    def compute_threshold(self, thresh=0.025, direction='below'):
        """Compute percentage of errors below a given threshold.
        direction: 'below', 'above'
        """

        percent = []
        for key, vals in self.errors.items():
            if direction == 'below':
                percent.append((sum(vals < thresh) / len(vals) * 100, key))
            elif direction == 'above':
                percent.append((sum(vals > thresh) / len(vals) * 100, key))
        percent.sort()
        percent.reverse()

        return percent


###################################################################################################
###################################################################################################

@CheckDims2D
def fit_ols(freqs, spectrum):
    """Fit spectrum with OlS, across whole range."""

    result = _ols_fit(freqs, spectrum)

    return result


@CheckDims2D
def fit_ols_alph(freqs, spectrum):
    """Fit spectrum with OlS, excluding pre-defined alpha band."""

    freqs, spectrum = exclude_spectrum(freqs, spectrum, ALPHA_RANGE)

    result = _ols_fit(freqs, spectrum)

    return result


@CheckDims2D
def fit_ols_oscs(freqs, spectrum):
    """Fit spectrum with OlS, ignoring specparam derived oscillation bands."""

    _, cens, _, bws = _specparam_fit(freqs, spectrum)
    freqs, spectrum = _drop_oscs(freqs, spectrum, cens, bws)

    result = _ols_fit(freqs, spectrum)

    return result


@CheckDims2D
def fit_ransac(freqs, spectrum):
    """Fit spectrum with RANSAC, across whole range."""

    result = _ransac_fit(freqs, spectrum)

    return result


@CheckDims2D
def fit_ransac_alph(freqs, spectrum):
    """Fit spectrum with RANSAC, excluding pre-defined alpha band."""

    freqs, spectrum = exclude_spectrum(freqs, spectrum, ALPHA_RANGE)

    result = _ransac_fit(freqs, spectrum)

    return result


@CheckDims2D
def fit_ransac_oscs(freqs, spectrum):
    """Fit spectrum with RANSAC, ignoring specparam derived oscillation bands."""

    _, cens, _, bws = _specparam_fit(freqs, spectrum)
    freqs, spectrum = _drop_oscs(freqs, spectrum, cens, bws)

    result = _ransac_fit(freqs, spectrum)

    return result


@CheckDims2D
def fit_rlm(freqs, spectrum):
    """Fit spectrum with RLM, across whole range."""

    result = _rlm_fit(freqs, spectrum)

    return result


@CheckDims2D
def fit_rlm_alph(freqs, spectrum):
    """Fit spectrum with RLM, excluding pre-defined alpha band."""

    freqs, spectrum = exclude_spectrum(freqs, spectrum, ALPHA_RANGE)

    result = _rlm_fit(freqs, spectrum)

    return result


@CheckDims2D
def fit_rlm_oscs(freqs, spectrum):
    """Fit spectrum with RLM, ignoring specparam derived oscillation bands."""

    _, cens, _, bws = _specparam_fit(freqs, spectrum)
    freqs, spectrum = _drop_oscs(freqs, spectrum, cens, bws)

    result = _rlm_fit(freqs, spectrum)

    return result


@CheckDims1D
def fit_exp(freqs, spectrum):
    """Fit spectrum with an exponential fit."""

    result = _exp_fit(freqs, spectrum)

    return result


@CheckDims1D
def fit_exp_alph(freqs, spectrum):
    """Fit spectrum with an exponential fit, excluding pre-defined alpha band."""

    freqs, spectrum = exclude_spectrum(freqs, spectrum, ALPHA_RANGE, make_2D=False)

    result = _exp_fit(freqs, spectrum)

    return result


@CheckDims1D
def fit_exp_oscs(freqs, spectrum):
    """Fit spectrum with an exponential fit, ignoring specparam derived oscillation bands."""

    _, cens, _, bws = _specparam_fit(freqs, spectrum)
    freqs, spectrum = _drop_oscs(freqs, spectrum, cens, bws)

    freqs = np.squeeze(freqs)
    spectrum = np.squeeze(spectrum)

    result = _exp_fit(freqs, spectrum)

    return result


@CheckDims1D
def fit_specparam(freqs, spectrum):
    """Fit spectral parameterization."""

    f_res = _specparam_fit(freqs, spectrum)
    result = -f_res[0]

    return result

###################################################################################################
###################################################################################################

def _ols_fit(freqs, spectrum):
    """Helper function for fitting OLS."""

    fx = sm.add_constant(np.log10(freqs))

    ols_model = sm.OLS(np.log10(spectrum), fx).fit()
    result = ols_model.params[1]

    return result


def _rlm_fit(freqs, spectrum):
    """Helper function for fitting RLM."""

    fx = sm.add_constant(np.log10(freqs))
    fit_rlm_out = sm.RLM(np.log10(spectrum), fx).fit()
    result = fit_rlm_out.params[1]

    return result


def _ransac_fit(freqs, spectrum):
    """"Helper function for fitting RANSAC."""

    ransac_model = RANSACRegressor(random_state=42)
    ransac_model.fit(np.log10(freqs), np.log10(spectrum))
    result = ransac_model.estimator_.coef_[0][0]

    return result


def _exp_fit(freqs, spectrum):
    """Helper function for fitting exponential."""

    fit_exp_out, _ = curve_fit(expf, freqs, np.log10(spectrum), p0=[1, 1])
    result = -fit_exp_out[1]

    return result


@CheckDims1D
def _specparam_fit(freqs, spectrum):
    """Helper function for fitting spectral parameterization."""

    fm = FOOOF(peak_width_limits=[1, 8], max_n_peaks=6, verbose=False)
    fm.fit(freqs, spectrum, [freqs.min(), freqs.max()])

    if len(fm.gaussian_params_ > 0):
        cfs, pws, bws = \
            fm.gaussian_params_[:, 0], fm.gaussian_params_[:, 1], fm.gaussian_params_[:, 2]
    else:
        cfs, pws, bws = np.array([]), np.array([]), np.array([])

    return fm.aperiodic_params_[1], cfs, pws, bws


def _drop_oscs(freqs, spectrum, cfs, bws):
    """Drop osc bands from spectrum."""

    m = 2.0
    for cf, bw in zip(cfs, bws):
        freqs, spectrum = exclude_spectrum(freqs, spectrum, [cf - m * bw, cf + m * bw])

    return freqs, spectrum
