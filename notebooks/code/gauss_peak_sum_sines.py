import numpy as np
from scipy.linalg import norm
import matplotlib.pyplot as plt
from neurodsp.utils.data import create_times
from neurodsp.utils.norm import demean, normalize_variance
from neurodsp.plts import plot_power_spectra, plot_time_series
from neurodsp.sim import sim_combined
from neurodsp.spectral import compute_spectrum

def sim_gauss_peak(n_seconds, fs, chi, central_freq, bw, ht):
	"""
	Returns a time series whose full power spectrum consists of a power law with exponent chi
	and a gaussian peak at central_freq with standard deviation bw and relative height ht.
	

	Parameters
    -----------
	n_seconds: float
		Number of seconds elapsed in the time series.
	fs: float
		Sampling rate.
	chi: float
		Power law exponent.
	central_freq: float
		Central frequency for the gaussian peak in Hz.
	bw: float
		Bandwidth, or standard deviation, of gaussian peak in Hz.
	ht: float
		Relative height in log_10(Hz) over the aperiodic component of the gaussian peak at central_freq.

	Returns
    -------
    sig: 1d array
    	Time series with desired power spectrum.
	"""

	times = create_times(n_seconds, fs)

	# Construct the aperiodic component and compute its Fourier transform. Only use the
	# first half of the frequencies from the Fourier transform since the signal is real.
	sig_components = {'sim_powerlaw': {'exponent': chi}}
	sig_ap = sim_combined(n_seconds, fs, sig_components)
	sig_len = sig_ap.shape[0]

	sig_ap_hat = np.fft.fft(sig_ap)[0:(sig_len//2+1)]

	# Create the range of frequencies that appear in the power spectrum since these
	# will be the frequencies in the cosines we sum below
	freqs = np.linspace(0, fs/2, num=sig_len//2 + 1, endpoint=True)

	# Construct the array of relative heights above the aperiodic power spectrum
	rel_heights = np.array([ ht * np.exp(-(f - central_freq)**2/(2*bw**2)) for f in freqs])

	# Build an array of the sum of squares of the cosines as they appear in the calculation of the
	# amplitudes
	cosine_norms = np.array([
						  norm(
						  	np.cos(2*np.pi*f*times), 2
						  )**2 for f in freqs
						])

	# Build an array of the amplitude coefficients
	cosine_coeffs = np.array([
					(-np.real(sig_ap_hat[ell]) + np.sqrt(np.real(sig_ap_hat[ell])**2 + (10**rel_heights[ell] - 1)*np.abs(sig_ap_hat[ell])**2))/cosine_norms[ell]
					for ell in range(cosine_norms.shape[0])]
				)

	# Add cosines with the respective coefficients and with a random phase shift for each one
	sig_periodic = np.sum(
					np.array(
						[cosine_coeffs[ell]*np.cos(2*np.pi*freqs[ell]*times + 2*np.pi*np.random.rand()) for ell in range(cosine_norms.shape[0])]
					),
					axis=0
					)

	# Normalize the signal
	sig = sig_ap + sig_periodic
	sig = demean(sig)
	sig = normalize_variance(sig)

	return sig

n_seconds = 50
fs = 500
chi = -2
central_freq = 20
bw = 5
ht = 7
sig = sim_gauss_peak(n_seconds, fs, chi, central_freq, bw, ht)
freqs, psd = compute_spectrum(sig, fs, nperseg=fs*n_seconds)
times = create_times(n_seconds, fs)

fig, axes = plt.subplots(2,1, figsize=(15,10))
plot_time_series(times, sig, ax=axes[0])
plot_power_spectra(freqs, psd, ax=axes[1])
