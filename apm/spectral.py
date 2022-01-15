"""Fitting simulated power spectra."""

import warnings

import numpy as np
from scipy.stats import ranksums

from apm.utils import abs_err
from apm.fit import (fit_ols, fit_ols_alph, fit_ols_oscs,
                     fit_rlm, fit_rlm_alph, fit_rlm_oscs,
                     fit_ransac, fit_ransac_alph, fit_ransac_oscs,
                     fit_exp, fit_exp_alph, fit_exp_oscs, fit_fooof)

###################################################################################################
###################################################################################################

class SpectralFits():
    """Class object for fitting power spectra using multiple methods."""

    def __init__(self):
        """Initialize object."""

        self.fit_funcs = {'OLS': fit_ols,
                          'OLS-EA': fit_ols_alph,
                          'OLS-EO': fit_ols_oscs,
                          'RLM': fit_rlm,
                          'RLM-EA': fit_rlm_alph,
                          'RLM-EO': fit_rlm_oscs,
                          'RAN': fit_ransac,
                          'RAN-EA': fit_ransac_alph,
                          'RAN-EO': fit_ransac_oscs,
                          'EXP': fit_exp,
                          'EXP-EA': fit_exp_alph,
                          'EXP-EO': fit_exp_oscs,
                          'FOOOF': fit_fooof}
        self.initialize_error_dict(0)


    def __add__(self, other):
        """Overload addition, to add errors fit across different datasets."""

        out = SimFits()

        for key, vals in other.errors.items():
            out.errors[key] = np.append(self.errors[key], other.errors[key])

        return out


    def __len__(self):
        """"Define length of the object as the number of computed errors."""

        return len(self.errors[self.errors.keys()[0]])


    def initialize_error_dict(self, n_psds):
        """Create a dictionary to store fitting errors."""

        self.errors = dict()
        for key in self.fit_funcs.keys():
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
                        self.errors[ki][ind] = 0


    def compare_errors(self):
        """Compare error distributions between methods."""

        comps = np.zeros([len(self.errors), len(self.errors)])

        for ii, ki in enumerate(self.errors.keys()):
            for ij, kj in enumerate(self.errors.keys()):
                s, p = ranksums(self.errors[ki], self.errors[kj])
                comps[ii, ij] = p

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
            std_errors.append((np.std(vals), key))
        std_errors.sort()

        return std_errors


    def compute_threshold(self, thresh=0.025):
        """Compute percentage of errors below a given threshold."""

        perc_good = []
        for key, vals in self.errors.items():
            perc_good.append((sum(vals < thresh) / len(vals), key))
        perc_good.sort()
        perc_good.reverse()

        return perc_good
