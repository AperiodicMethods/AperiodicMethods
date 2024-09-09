"""Precompute a set of simulations.

Some time series simulations are quite slow.
And/or we might want to test multiple different analyses on the exact same set of simulations.
To support this, here we pre-generate simulations that can be reloaded when needed.
"""

from neurodsp.sim.aperiodic import sim_powerlaw, sim_synaptic_current, sim_knee
from neurodsp.sim.combined import sim_combined, sim_combined_peak
from neurodsp.sim.multi import sim_multi_across_values
from neurodsp.sim.io import save_sims
from neurodsp.utils import set_random_seed

# Import custom code
import sys; from pathlib import Path
sys.path.append(str(Path('..').resolve()))
from apm.io import APMDB, save_pickle
from apm.sim.defs import SIM_ITERS
from apm.sim.settings import N_SIMS, FS, FS2

###################################################################################################
###################################################################################################

# Set whether to replace any existing simulations
REPLACE = True

# Settings for saving out simulations
SIMPATH = APMDB().sims_path / 'time_series'

###################################################################################################
###################################################################################################

def main():

    set_random_seed(101)

    print('\nCREATING SIMULATIONS...\n')

    for cfs in [FS, FS2]:

        print('\tcreating simulations with fs of {}:'.format(cfs))
        SIM_ITERS.update_base(fs=cfs)

        # Simulate a predefined set of exponent variation simulations
        print('\t\tcreating exponent simulations...')
        sigs_ap = sim_multi_across_values(sim_powerlaw, SIM_ITERS['ap_exp'], N_SIMS)
        save_sims(sigs_ap, 'ap-exp-' + str(cfs), SIMPATH, REPLACE)

        # Simulate a predefined set of combined exponent variation simulations
        print('\t\tcreating combined simulations...')
        sigs_comb = sim_multi_across_values(sim_combined, SIM_ITERS['comb_exp'], N_SIMS)
        save_sims(sigs_comb, 'comb-exp-' + str(cfs), SIMPATH, REPLACE)

        # Simulate a predefined set of combined frequency variation simulations
        print('\t\tcreating frequency simulations...')
        sigs_freq = sim_multi_across_values(sim_combined, SIM_ITERS['osc_freq'], N_SIMS)
        save_sims(sigs_freq, 'comb-freq-' + str(cfs), SIMPATH, REPLACE)

        # Simulate a predefined set of combined oscillation power simulations
        print('\t\tcreating power simulations...')
        sigs_pow = sim_multi_across_values(sim_combined, SIM_ITERS['osc_pow'], N_SIMS)
        save_sims(sigs_pow, 'comb-pow-' + str(cfs), SIMPATH, REPLACE)

        # Simulate a predefined set of synaptic timescale variation simulations
        print('\t\tcreating synaptic timescale simulations...')
        sigs_tscales = sim_multi_across_values(\
            sim_synaptic_current, SIM_ITERS['syn_tscales'], N_SIMS)
        save_sims(sigs_tscales, 'ap-tscales-' + str(cfs), SIMPATH, REPLACE)

        # Simulate a predefined set of aperiodic knee variation simulations
        print('\t\tcreating knee simulations...')
        sigs_knee = sim_multi_across_values(sim_knee, SIM_ITERS['kn_knee'], N_SIMS)
        save_sims(sigs_knee, 'ap-knee-' + str(cfs), SIMPATH, REPLACE)

        # Simulate a predefined set of combined peak bandwidth variation simulations
        print('\t\tcreating bandwidth simulations...')
        sigs_bw = sim_multi_across_values(sim_combined_peak, SIM_ITERS['peak_bw'], N_SIMS)
        save_sims(sigs_bw, 'comb-bw-' + str(cfs), SIMPATH, REPLACE)

        # Simulate a predefined set of bursty oscillation simulations
        print('\t\tcreating bursty simulations...')
        sigs_burst = sim_multi_across_values(sim_combined, SIM_ITERS['comb_burst'], N_SIMS)
        save_sims(sigs_bw, 'comb-burst-' + str(cfs), SIMPATH, REPLACE)

        print('\tfinished simulations with fs of {}\n'.format(cfs))

    print('\nSIMULATIONS CREATED\n')


if __name__ == "__main__":
    main()
