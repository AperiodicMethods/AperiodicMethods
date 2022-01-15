"""Pre-generate some example time series."""

from neurodsp.utils import create_times
from neurodsp.sim import sim_powerlaw, sim_oscillation, sim_combined, sim_synaptic_current

from apm.sim.settings import N_SECONDS, FS, EXP, FREQ, SIM_PARAMS_COMB, SIM_PARAMS_BURST

###################################################################################################
###################################################################################################

TIMES = create_times(N_SECONDS, FS)
SIG_AP = sim_powerlaw(N_SECONDS, FS, EXP)
SIG_KN = sim_synaptic_current(N_SECONDS, FS)
SIG_OSC = sim_oscillation(N_SECONDS, FS, FREQ)
SIG_COMB = sim_combined(**SIM_PARAMS_COMB)
SIG_BURST = sim_combined(**SIM_PARAMS_BURST)
