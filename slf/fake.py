"""   """

from __future__ import print_function

import numpy as np
from slf.fit import *

from foof import syn

#########################################################################################
#########################################################################################

class SynFits():
    """  """

    def __init__(self):
        """   """

        self.fit_funcs = dict()
        self.errs = dict()


    def get_fit_funcs(self):
        """Initialize fit functions to use."""

        self.fit_funcs = {'RLM': fsl_rlm,
                          'RLM-EA': fsl_rlm_alph,
                          'RLM-EO': fsl_rlm_oscs,
                          'RAN': fsl_ransac,
                          'RAN-EA': fsl_ransac_alph,
                          'RAN-EO': fsl_ransac_oscs}


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
                self.errs[k][i] = sqd_err(-slv, fn(fs, psds[:, i]))


    def comp_errs(self):
        """   """

        pass


    def calc_mean_errs(self):
        """Calculate mean errors per method."""

        mean_errs = []
        for k, v in self.errs.items():
            mean_errs.append((np.median(v), k))
            #mean_errs.append((np.mean(v), k))
        mean_errs.sort()

        return mean_errs

#########################################################################################
#########################################################################################

def mk_psds(n_psds, slv):
    """Generate synthetic PSDs."""

    fs, psds = syn.synthesize(n_psds, fn=syn.mfonef,
                              mf=[10], mf_sig=[1], mk=[0.2], chi=slv,
                              f0=3, fmax=40, res=0.5, noi=0.05)

    return fs, psds


def print_errs(mean_errs):
    """Print out the mean errors per method."""

    print('\n')
    for me in mean_errs:
        print(me[1], '\t\t', me[0])
    print('\n')

#########################################################################################
#########################################################################################