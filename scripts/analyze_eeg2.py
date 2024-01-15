"""Analysis script for analyzing the developmental EEG dataset."""

from pathlib import Path

import numpy as np

# Import custom code
import sys
sys.path.append(str(Path('..').resolve()))
from apm.io import APMDB, save_pickle
from apm.data.measures import MEASURES, PEAK_MEASURES
from apm.analysis import compute_avgs, compute_all_corrs, compute_corrs_to_feature
from apm.run import run_group_measures

###################################################################################################
###################################################################################################

# Define the data folders
PROJECT = Path('/Users/tom/Documents/Research/2-Projects/1a-Current(Voytek)/AperiodicMethods/')
DATA_FOLDER = PROJECT / '2-Data/apm_data/eeg2'

# Settings for saving out results files
OUTPATH = APMDB().data_path / 'eeg2'

###################################################################################################
###################################################################################################

def main():

    print('\nANALYZING GROUP EEG DATA...')

    # Load data
    group_data = np.load(FOLDER_GROUP / 'MIPDB_extracted_block.npy')
    group_data = np.squeeze(group_data[:, 0, :, :])

    ## APERIODIC MEASURES

    # Compute results across the group
    group_results = run_group_measures(group_data, MEASURES)
    save_pickle(group_results, 'eeg2_results', OUTPATH)

    ## APERIODIC CORRELATIONS

    # Compute average and subselect time domain measures
    group_avg = compute_avgs(group_results)
    group_avg_ts = {ke : va for ke, va in group_avg.items() \
        if ke not in ['specparam', 'irasa']}

    # Compute and save group correlations
    group_corrs = compute_all_corrs(group_avg_ts)
    save_pickle(group_corrs, 'eeg2_spatial_corrs', OUTPATH)

    # Compute and save differences
    group_exp_corrs = compute_corrs_to_feature(group_avg_ts, group_avg['specparam'])
    save_pickle(group_exp_corrs, 'eeg2_spatial_exp_corrs', OUTPATH)

    ## PEAK MEASURES

    # Compute group level peak measures
    group_results_peaks = run_group_measures(group_data, PEAK_MEASURES)
    group_results_peaks['alpha_power'] = np.log10(group_results_peaks['alpha_power'])
    save_pickle(group_results_peaks, 'eeg2_results_peaks', OUTPATH)

    ## PEAK CORRELATIONS

    # Compute correlations between peak measures and time domain measures
    group_avg_peaks = compute_avgs(group_results_peaks)
    group_alpha_corrs = compute_corrs_to_feature(\
        group_avg_ts, group_avg_peaks['alpha_power'])
    save_pickle(group_alpha_corrs, 'eeg2_spatial_alpha_corrs', OUTPATH)

    # # Compute differences between peak correlations
    # group_alpha_corr_diffs = compute_diffs_to_feature(\
    #     group_avg_ts, group_avg_peaks['alpha_power'])
    # save_pickle(group_alpha_corr_diffs, 'eeg2_spatial_alpha_corrs_diffs', OUTPATH)

    print('COMPLETED GROUP EEG DATA ANALYSES\n')


if __name__ == "__main__":
    main()
