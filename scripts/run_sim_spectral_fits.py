"""Run script for fitting simualted across, testing multiple methods."""

from apm import syn
from apm.fake import SynFits
from apm.core.db import APMDB
from apm.core.io import save_pickle

###################################################################################################
###################################################################################################

# Spectrum Settings
N_SPECTRA = 100
F_RANGE = [3, 40]

# Simulation Settings
NOISE_VALS = [0.0, 0.01, 0.05, 0.1, 0.15, 0.2]
EXP_VALS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

###################################################################################################
###################################################################################################

def main():

    db = APMDB()

    for exp in EXP_VALS:
        for noise in NOISE_VALS:

            print('Running sims for exponent val {}, noise-val {}'.format(slv, nslv))

            # Initialize syn-fitter object
            syns = SynFits()
            syns.get_fit_funcs()

            # Generate the power spectra
            freqs, psds = syn.sim_n_psds(N_SPECTRA, F_RANGE, exp, syn.gen_osc_def(), noise)

            # Fit spectra
            syns.fit_spectra(exp, freqs, psds)

            # Save out fit data
            save_name = 'SynFits_slv' + str(exp) + '_N' + str(noise) + '.p'
            save_pickle(syns.errs, save_name, db.syns_path)

if __name__ == '__main__':
    main()
