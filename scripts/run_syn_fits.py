"""   """

from slf import syn
from slf.fake import SynFits, print_errs

#########################################################################################
#########################################################################################

# PSD SETTINGS
N_PSDS = 2
F_RANGE = [3, 40]

# Simulation Settings
NOISE_VALS = [0, 0.01, 0.05, 0.1, 0.15, 0.2]
SLOPE_VALS = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

#########################################################################################
#########################################################################################

def main():

    for slv in SLOPE_VALS:
        for nslv in NOISE_VALS:

            # Initialize syn-fitter object
            syns = SynFits()
            syns.get_fit_funcs()

            # Generate the PSDs
            freqs, psds = syn.sim_n_psds(N_PSDS, F_RANGE, slv, syn.gen_osc_def(), nslv)

            # Fit slopes
            syns.fit_slopes(slv, freqs, psds)

            #
            avgs = syns.calc_avg_errs()
            print_errs(avgs)

if __name__ == '__main__':
    main()
