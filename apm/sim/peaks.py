"""Code for simulating peaks."""

import pkg_resources

import numpy as np

###################################################################################################
###################################################################################################

N_PEAK_OPTS = [0, 1, 2, 3]
N_PEAK_PROBS = [1/4, 1/4, 1/4, 1/4]

CF_OPTS = np.load(pkg_resources.resource_filename(__name__, 'data/freqs.npy'))
CF_PROBS = np.load(pkg_resources.resource_filename(__name__, 'data/probs.npy'))

PW_OPTS = [0.15, 0.25, 0.5, 1.0, 1.5]
PW_PROBS = [0.2, 0.2, 0.2, 0.2, 0.2]

BW_OPTS = [1, 1.5, 2, 2.5]
BW_PROBS = [1/4, 1/4, 1/4, 1/4]

###################################################################################################
###################################################################################################

def gen_peak_def(n_peaks=None):
    """Generate a plausible peak distribution for a simulated power spectrum.

    Parameters
    ----------
    n_peaks : int, optional, default: None
        Number of peaks to generate. If None, picked at random.

    Yields
    ------
    peaks : [] or list of list of [float, float, float]
        Peak definitions.

    Notes
    -----
    This function samples peak definitions based on a distribution of
    center frequency values observed in a large dataset of MEG data.
    """

    while True:

        # If not predetermined, randomly choose how many peaks to add
        #   This uses a new variable so that it re-checks samples across iterations
        if n_peaks is None:
            n_peaks_sim = np.random.choice(N_PEAK_OPTS, p=N_PEAK_PROBS)
        else:
            n_peaks_sim = n_peaks

        # Generate peak definitions
        peaks = []
        for ind in range(n_peaks_sim):

            cur_cf = np.random.choice(CF_OPTS, p=CF_PROBS)

            while _check_duplicate(cur_cf, [it[0] for it in peaks]):
                cur_cf = np.random.choice(CF_OPTS, p=CF_PROBS)

            cur_pw = np.random.choice(PW_OPTS, p=PW_PROBS)
            cur_bw = np.random.choice(BW_OPTS, p=BW_PROBS)

            peaks.append([cur_cf, cur_pw, cur_bw])

        yield peaks


def _check_duplicate(cur_cf, all_cfs, window=1):
    """Check if a candidate center frequency has already been chosen.

    Parameters
    ----------
    cur_cf : float
        Candidate center frequency.
    all_cfs : list of float
        Already chosen center frequencies.
    window : int, optional
        Window around the candidate to check if already exists chosen centers.

    Returns
    -------
    bool
        Whether the candidate center frequency is already included.
    """

    if len(all_cfs) == 0:
        return False
    for ch in range(cur_cf - window, cur_cf + window + 1):
        if ch in all_cfs:
            return True

    return False
