"""Analysis script for analyzing the developmental EEG dataset."""

from pathlib import Path

import numpy as np

from fooof import FOOOFGroup, fit_fooof_3d
from neurodsp.spectral import compute_spectrum

# Import custom code
import sys
sys.path.append(str(Path('..').resolve()))
from apm.io import APMDB, save_pickle
from apm.analysis import (compute_avgs, compute_all_corrs,
                          compute_corrs_to_feature, compute_diffs_to_feature)
from apm.run import run_group_measures
from apm.methods import irasa
from apm.methods.settings import ALPHA_RANGE
from apm.methods.periodic import get_fm_peak_power

# Import general settings from script settings
from settings import TS_MEASURES, SPECPARAM_SETTINGS

###################################################################################################
###################################################################################################

## PATH SETTINGS

# Define the data folders
PROJECT = Path('/Users/tom/Documents/Research/2-Projects/1a-Current(Voytek)/AperiodicMethods/')
DATA_FOLDER = PROJECT / '2-Data/apm_data/eeg2'

# Settings for saving out results files
OUTPATH = APMDB().data_path / 'eeg2'

## DATA PROPERTIES

# Define sampling frequency of current dataset
FS = 500

## METHOD SETTINGS

FIT_RANGE = [3, 40]

PSD_SETTINGS = {
    'fs' : FS,
    'nperseg' : 2 * FS,
    'noverlap' : FS,
}

IRASA_SETTINGS = {
    'fs' : FS,
    'f_range' : FIT_RANGE,
    'fit_func' : 'fit_irasa_exp',
}

IRASA_MEASURES = {
    irasa : IRASA_SETTINGS,
}

MEASURES = TS_MEASURES | IRASA_MEASURES

###################################################################################################
###################################################################################################

def main():

    print('\nANALYZING GROUP EEG DATA...')

    # Load data
    data = np.load(DATA_FOLDER / 'MIPDB_extracted_block.npy')
    data = np.squeeze(data[:, 0, :, :])

    ## APERIODIC MEASURES

    # Compute results across the group
    results = run_group_measures(data, MEASURES)

    # Run specparam
    freqs, powers = compute_spectrum(data, **PSD_SETTINGS)
    fg = FOOOFGroup(**SPECPARAM_SETTINGS)
    fgs = fit_fooof_3d(fg, freqs, powers, FIT_RANGE)
    for ind, fg in enumerate(fgs):
        fg.save('eeg2_specparam_' + str(ind).zfill(2), OUTPATH / 'specparam', save_results=True)
    results['specparam'] = np.array([cfg.get_params('aperiodic', 'exponent') for cfg in fgs])

    save_pickle(results, 'eeg2_results', OUTPATH)

    ## PEAK MEASURES

    # Extract and collect the peak alpha power per channel
    results_peaks = {'alpha_power' : np.zeros([len(fgs), len(fg)])}
    for s_ind, fg in enumerate(fgs):
        for c_ind in range(len(fg)):
            results_peaks['alpha_power'][s_ind, c_ind] = \
                get_fm_peak_power(fg.get_fooof(c_ind), ALPHA_RANGE)

    save_pickle(results_peaks, 'eeg2_results_peaks', OUTPATH)

    ## SPATIAL MEASURES

    # Compute average and subselect time domain measures
    group_avg = compute_avgs(results)
    group_avg_ts = {ke : va for ke, va in group_avg.items() \
        if ke not in ['specparam', 'irasa']}

    # Compute and save spatial correlations across time domain measures
    group_corrs = compute_all_corrs(group_avg_ts)
    save_pickle(group_corrs, 'eeg2_spatial_corrs', OUTPATH)

    # Compute and save spatial correlations between time domain and exponent measures
    group_exp_corrs = compute_corrs_to_feature(group_avg_ts, group_avg['specparam'])
    save_pickle(group_exp_corrs, 'eeg2_spatial_exp_corrs', OUTPATH)

    ## SPATIAL MEASURES: PERIODIC

    # Compute correlations between peak measures and time domain measures
    group_avg_peaks = compute_avgs(results_peaks)
    group_alpha_corrs = compute_corrs_to_feature(\
        group_avg_ts, group_avg_peaks['alpha_power'])
    save_pickle(group_alpha_corrs, 'eeg2_spatial_alpha_corrs', OUTPATH)

    # Compute differences between peak correlations
    group_alpha_corr_diffs = compute_diffs_to_feature(\
        group_avg_ts, group_avg_peaks['alpha_power'])
    save_pickle(group_alpha_corr_diffs, 'eeg2_spatial_alpha_corrs_diffs', OUTPATH)

    print('COMPLETED GROUP EEG DATA ANALYSES\n')


if __name__ == "__main__":
    main()
