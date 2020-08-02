"""Fitting simulated power spectra."""

import numpy as np
from scipy.stats import ranksums

from apm.fit import *
from apm.utils import *

###################################################################################################
###################################################################################################

class SimFits():
    """Class object for fitting power spectra using multiple methods."""

    def __init__(self):
        """Initialize object."""

        self.fit_funcs = dict()
        self.errs = dict()


    def __add__(self, other):
        """Overload addition, to add errors fit across different datasets."""

        out = SimFits()
        out.get_fit_funcs()

        for key, vals in other.errs.items():
            out.errs[key] = np.append(self.errs[key], other.errs[key])

        return out


    def get_fit_funcs(self):
        """Initialize fit functions to use."""

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


    def get_err_dict(self, n_psds):
        """Create a dictionary to store fitting errors."""

        self.errs = dict()
        for key in self.fit_funcs.keys():
            self.errs[key] = np.zeros(n_psds)


    def fit_spectra(self, exp, fs, psds):
        """Fit spectra with available methods."""

        _, n_psds = psds.shape
        self.get_err_dict(n_psds)

        for ki, fn in self.fit_funcs.items():
            for ind in range(n_psds):
                try:
                    #self.errs[ki][ind] = sqd_err(-exp, fn(fs, psds[:, ind]))
                    self.errs[ki][ind] = abs_err(-exp, fn(fs, psds[:, ind]))
                except:
                    self.errs[ki][ind] = 0


    def comp_errs(self):
        """Compare error distributions between methods."""

        comps = np.zeros([len(self.errs), len(self.errs)])

        for ii, ki in enumerate(self.errs.keys()):
            for ij, kj in enumerate(self.errs.keys()):
                s, p = ranksums(self.errs[ki], self.errs[kj])
                comps[ii, ij] = p

        return comps


    def calc_avg_errs(self, avg='median'):
        """Calculate average errors per method."""

        avg_errs = []
        for key, vals in self.errs.items():
            if avg == 'median':
                avg_errs.append((np.nanmedian(vals), key))
            elif avg == 'mean':
                avg_errs.append((np.nanmean(vals), key))
            else:
                raise ValueError('Average type not understood')
        avg_errs.sort()

        return avg_errs


    def calc_perc_good(self, thresh=0.025):
        """Calculate percentage of errors below some threshold."""

        perc_good = []
        for key, vals in self.errs.items():
            perc_good.append((sum(vals < thresh) / len(vals), key))
        perc_good.sort()
        perc_good.reverse()

        return perc_good

###################################################################################################
###################################################################################################

def print_res(data):
    """Print out the mean errors per method."""

    for it in data:
        print('   {:8} \t\t {:1.5f}'.format(it[1], it[0]))
