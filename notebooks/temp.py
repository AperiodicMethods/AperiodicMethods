## Fitting Helper Functions

import numpy as np

from scipy.optimize import curve_fit

from neurodsp.sim import sim_combined
from neurodsp.utils.data import create_times
from neurodsp.aperiodic import compute_irasa, fit_irasa


def log_space_freqs(freqs, n_points):
    """Given an array of frequency values, returns a subset of those frequency values which are approximately
    equispaced logarithmically.

    Parameters
    ----------
    freqs : xx
        xx
    n_points : xx
        xx

    Returns
    -------
    log_freqs : xx
        xx
    """

    # Grab the lowest and highest frequencies to form a logarithmic grid of frequencies
    #   not necessarily corresponding to frequencies in the array freqs
    f_start, f_end = freqs[0], freqs[-1]
    log_grid = np.logspace(np.log10(f_start), np.log10(f_end), n_points)

    # For every element in log_grid, find the closest element in freqs
    log_freq_indices = np.array([np.argmin(np.abs(log_freq - freqs)) for log_freq in log_grid]).astype('int')
    log_freqs = freqs[log_freq_indices]

    # Throw out any duplicates
    log_freqs = np.unique(log_freqs)

    return log_freqs


def fit_func(freqs, intercept, slope):
    """A fit function to use for fitting IRASA separated 1/f power spectra components."""

    return slope * freqs + intercept


def knee_func(freqs, offset, chi1, chi2, knee):
    """
    Logarithm base 10 of the function

    offset * 1/(freqs**chi1 * (freqs**chi2 + knee))

    used to fit a knee model.
    """

    return np.log10(offset) - chi1*np.log10(freqs) - np.log10(freqs**chi2 + knee)


def fit_irasa_logspace(freqs, psd_aperiodic):
    """Fit the IRASA derived aperiodic component of the spectrum.

    The fitting uses logarithmically spaced frequencies.
    This is basically copied from NeuroDSP's implementation with only a minor modification before
    the spectral fitting.

    Parameters
    ----------
    freqs : 1d array
        Frequency vector, in linear space.
    psd_aperidic : 1d array
        Power values, in linear space.

    Returns
    -------
    intercept : float
        Fit intercept value.
    slope : float
        Fit slope value.

    Notes
    -----
    This fits a linear function of the form `y = ax + b` to the log-log aperiodic power spectrum.
    """

    # Grab log spaced frequencies. Subsample by a factor of 2.
    resampled_freqs = log_space_freqs(freqs, freqs.shape[0]//2)

    # Grab the corresponding indices to resample the psd.
    resampled_idxs = np.array([np.argmin(np.abs(resampled_freq - freqs)) for resampled_freq in resampled_freqs])
    resampled_psd = psd_aperiodic[resampled_idxs]

    popt, _ = curve_fit(fit_func, np.log10(resampled_freqs), np.log10(resampled_psd))
    intercept, slope = popt

    return intercept, slope


def fit_irasa_knee(freqs, psd_aperiodic):

    # Force non-negative parameters.
    lower_bounds = np.array([0, 0, 0, 0])
    upper_bounds = np.array([10, 5, 5, np.inf])

    # Dont feed in logarithmic frequencies.
    popt, _ = curve_fit(knee_func, freqs, np.log10(psd_aperiodic), bounds=(lower_bounds, upper_bounds))
    offset, chi1, chi2, knee = popt

    return offset, chi1, chi2, knee


##  Experiment functions

def multiple_sines_trial(n_seconds, fs, chi, sine_freqs, f_range=None, log_space_irasa=False):
    """Generates a time series with power law exponent chi and sinusoids with frequencies sine_freqs
    and returns the estimated power law exponent using IRASA.
    """

    times = create_times(n_seconds, fs)

    # Collect IRASA settings
    irasa_params = {'fs' : fs, 'f_range' : f_range}
    sim_components = {'sim_powerlaw': {'exponent' : chi},
                      'sim_oscillation': [{'freq' : sine_freq} for sine_freq in sine_freqs]}
    sig = sim_combined(n_seconds, fs, sim_components)


    freqs_irasa, psd_ap, psd_pe = compute_irasa(sig, **irasa_params)
    fit_off, fit_exp = fit_irasa(freqs_irasa, psd_ap) if not log_space_irasa else fit_irasa_logspace(freqs_irasa, psd_ap)

    return fit_exp


def central_frequency_trial(n_seconds, fs, f_range, chi, central_freq, ht, bw, seed=None):
    """
    Generates a time series with power law exponent chi and sinusoids with frequencies sine_freqs
    and returns the estimated power law exponent using IRASA.
    """

    times = create_times(n_seconds, fs)

    # Collect IRASA settings
    irasa_params = {'fs' : fs, 'f_range' : f_range}
    if seed is not None:
        np.random.seed(seed)
    sig = sim_central_freq(n_seconds, fs, chi, central_freq, bw, ht)

    freqs_irasa, psd_ap, psd_pe = compute_irasa(sig, **irasa_params)
    fit_off, fit_exp = fit_irasa(freqs_irasa, psd_ap)

    return fit_exp


def knee_trial(n_seconds, fs, f_range=None, **sim_knee_kwargs):
    """
    Generates a time series with power law exponent chi and sinusoids with frequencies sine_freqs
    and returns the estimated power law exponent using IRASA.
    """

    times = create_times(n_seconds, fs)

    # Collect IRASA settings
    irasa_params = {'fs' : fs, 'f_range' : f_range}
    sig = sim_knee(n_seconds, fs, **sim_knee_kwargs)


    freqs_irasa, psd_ap, psd_pe = compute_irasa(sig, **irasa_params)
    fit_offset, fit_chi1, fit_chi2, fit_knee = fit_irasa_knee(freqs_irasa, psd_ap)

    return fit_chi1, fit_chi2, fit_knee


## Parallel Functions

from functools import partial
from multiprocessing import Pool, cpu_count
from tqdm.notebook import tqdm

N_SECONDS = 30
FS = 500
F_RANGE = (3, 40)

def _proxy(parameter_grid, n_seconds=N_SECONDS, fs=FS, f_range=F_RANGE):
    """Allows easier mapping of grid params.

    Notes
    -----
    In central_frequency_trial would return the same value when the first four params were the same,
    but only for the parallel_func, and not when running serially.
    i.e. array([[-0.,  1.,  0.,  1.,  0.],
                [-0.,  1.,  0.,  1.,  1.],
                [-0.,  1.,  0.,  1.,  2.]])

    I added a seed arg to central_frequency_trial so random signals could be simulated.
    Not sure why multiprocessing returns the same values without this, or how it sets
    random seeds, esp since it's not a prob when running serially.

    Anyways, the seed arg is a hack to ensure diff values during simulation.
    """

    return central_frequency_trial(n_seconds, fs, f_range, *parameter_grid[:-1],
                                   seed=int(np.random.randint(100000) + parameter_grid[-1]))


def parallel_func(n_jobs=-1, parameter_grid=None):
    """"Compute exponents in parallel.

    Parameters
    ----------
    n_jobs : int, optional, default: -1
        Number of jobs to run in parallel
        (i.e number of cores of threads if cores are hyperthreaded)
        Defaults to maximum, in my case 12 jobs (6 hyperthreaded cores).
    """
    n_jobs = cpu_count() if n_jobs == -1 else n_jobs

    with Pool(processes=n_jobs) as pool:

        # If you run out of memory, use imap instead of map.
        mapping = pool.map(partial(_proxy, n_seconds=N_SECONDS, fs=FS, f_range=F_RANGE),
                           parameter_grid)
        fit_exps = list(tqdm(mapping, desc="Fitting Exponents", total=len(parameter_grid), dynamic_ncols=True))

    return fit_exps
