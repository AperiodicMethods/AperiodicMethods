"""Pre-generate some example time series."""

from neurodsp.utils import create_times
from neurodsp.sim import (sim_powerlaw, sim_synaptic_current, sim_oscillation,
                          sim_combined, sim_peak_oscillation)

from apm.sim.sim import sim_combined_peak
from apm.sim.settings import (N_SECONDS, FS, EXP, FREQ,
                              SIM_PARAMS_COMB, SIM_PARAMS_BURST, SIM_PARAMS_PEAK)

###################################################################################################
###################################################################################################

# Times vector
TIMES = create_times(N_SECONDS, FS)

# Aperiodic time series
SIG_AP = sim_powerlaw(N_SECONDS, FS, EXP)
SIG_KN = sim_synaptic_current(N_SECONDS, FS)

# Oscillatory time series
SIG_OSC = sim_oscillation(N_SECONDS, FS, FREQ)

# Combined time series
SIG_COMB = sim_combined(**SIM_PARAMS_COMB)
SIG_BURST = sim_combined(**SIM_PARAMS_BURST)
SIG_PEAK = sim_combined_peak(**SIM_PARAMS_PEAK)
