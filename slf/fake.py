"""Fitting synthethic data."""

import numpy as np
from scipy.stats import ranksums

from slf.fit import *

#########################################################################################
#########################################################################################

class SynFits():
    """Class object for slope fitting synthetic data with multiple methods."""

    def __init__(self):
        """Initialize object."""

        self.fit_funcs = dict()
        self.errs = dict()


    def __add__(self, other):
        """Overload addition, to add errors fit across different datasets."""

        out = SynFits()
        out.get_fit_funcs()

        for key, vals in other.errs.items():
            out.errs[key] = np.append(self.errs[key], other.errs[key])

        return out


    def get_fit_funcs(self):
        """Initialize fit functions to use."""

        self.fit_funcs = {'OLS': fsl_ols,
                          'RLM': fsl_rlm,
                          'RLM-EA': fsl_rlm_alph,
                          'RLM-EO': fsl_rlm_oscs,
                          'RAN': fsl_ransac,
                          'RAN-EA': fsl_ransac_alph,
                          'RAN-EO': fsl_ransac_oscs,
                          'EXP': fsl_exp,
                          'EXP-EA': fsl_exp_alph,
                          'EXP-EO': fsl_exp_oscs,
                          'FOOOF': fsl_fooof}


    def get_err_dict(self, n_psds):
        """Create a dictionary to store fitting errors."""

        self.errs = dict()
        for key in self.fit_funcs.keys():
            self.errs[key] = np.zeros(n_psds)


    def fit_slopes(self, slv, fs, psds):
        """Fit PSD slopes with available methods."""

        _, n_psds = psds.shape
        self.get_err_dict(n_psds)

        for k, fn in self.fit_funcs.items():
            for i in range(n_psds):
                #self.errs[k][i] = sqd_err(-slv, fn(fs, psds[:, i]))
                self.errs[k][i] = abs_err(-slv, fn(fs, psds[:, i]))


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
            perc_good.append((sum(vals < 0.025) / len(vals), key))
        perc_good.sort()
        perc_good.reverse()

        return perc_good

#########################################################################################
#########################################################################################

def print_res(dat):
    """Print out the mean errors per method."""

    for it in dat:
        print('   {:8} \t\t {:1.5f}'.format(it[1], it[0]))

#########################################################################################
#########################################################################################