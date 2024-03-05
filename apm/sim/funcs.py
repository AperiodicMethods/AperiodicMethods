"""Additional simulation functions.

NOTE: This code is a candidate for moving to NDSP.
"""

from neurodsp.sim.info import get_sim_func
from neurodsp.sim.combined import sim_peak_oscillation

###################################################################################################
###################################################################################################

def sim_combined_peak(n_seconds, fs, components):
    """Simulate a combined signal with an aperiodic component and a peak.

    Parameters
    ----------
    n_seconds : float
        Simulation time, in seconds.
    fs : float
        Sampling rate of simulated signal, in Hz.
    components : dict
        A dictionary of simulation functions to run, with their desired parameters.

    Returns
    -------
    sig : 1d array
        Simulated combined peak signal.
    """

    sim_names = list(components.keys())
    assert len(sim_names) == 2, 'Expected only 2 components.'
    assert sim_names[1] == 'sim_peak_oscillation', \
        'Expected `sim_peak_oscillation` as the second key.'

    ap_func = get_sim_func(sim_names[0]) if isinstance(sim_names[0], str) else sim_names[0]

    sig = sim_peak_oscillation(\
        ap_func(n_seconds, fs, **components[sim_names[0]]), fs, **components[sim_names[1]])

    return sig


# Alternative implementation of the above - probably to drop:
# def sim_combined_peak(n_seconds, fs, ap_func, ap_params, peak_params):

#     sig_ap = ap_func(n_seconds, fs, **ap_params)
#     sig = sim_peak_oscillation(sig_ap, fs, **peak_params)

#     return sig
