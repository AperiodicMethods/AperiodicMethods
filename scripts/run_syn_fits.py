"""Run script for fitting slope across synthetic PSDs, testing multiple methods."""

from slf import syn
from slf.fake import SynFits
from slf.core.db import SLFDB
from slf.core.io import save_pickle

#########################################################################################
#########################################################################################

# PSD SETTINGS
N_PSDS = 100
F_RANGE = [3, 40]

# Simulation Settings
NOISE_VALS = [0.0, 0.01, 0.05, 0.1, 0.15, 0.2]
SLOPE_VALS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

#########################################################################################
#########################################################################################

def main():

    db = SLFDB()

    for slv in SLOPE_VALS:
        for nslv in NOISE_VALS:

            # Print status
            print('Running sims for slope val {}, noise-val {}'.format(slv, nslv))

            # Initialize syn-fitter object
            syns = SynFits()
            syns.get_fit_funcs()

            # Generate the PSDs
            freqs, psds = syn.sim_n_psds(N_PSDS, F_RANGE, slv, syn.gen_osc_def(), nslv)

            # Fit slopes
            syns.fit_slopes(slv, freqs, psds)

            # Save out fit data
            save_name = 'SynFits_slv' + str(slv) + '_N' + str(nslv) + '.p'
            save_pickle(syns.errs, save_name, db.syns_path)

if __name__ == '__main__':
    main()
