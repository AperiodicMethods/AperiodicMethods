"""Analysis script for analyzing the developmental EEG dataset."""

from pathlib import Path

import numpy as np

# Import custom code
import sys
sys.path.append(str(Path('..').resolve()))
from apm.io import APMDB, get_files, save_pickle
from apm.data.measures import MEASURES, PEAK_MEASURES
from apm.analysis import (compute_avgs, compute_all_corrs,
                          compute_corrs_to_feature, compute_diffs_to_feature)
from apm.run import run_measures, run_group_measures

###################################################################################################
###################################################################################################

# Run settings
RUN_EXTRACTED = False
RUN_GROUP = True

# Define the data folders
PROJECT = Path('/Users/tom/Documents/Research/2-Projects/1a-Current(Voytek)/AperiodicMethods/')
DATA_FOLDER = PROJECT / '2-Data/apm_data/eeg2'

FOLDER_EXTRACTED = Path('/Users/tom/Data/VoytekLab/ExtractedSubsets/childmind/')
FOLDER_GROUP = Path('/Users/tom/Documents/Research/2-Projects/1a-Current(Voytek)/AperiodicMethods/2-Data/apm_data/eeg2')

# Settings for saving out results files
OUTPATH = APMDB().data_path / 'eeg2'

###################################################################################################
###################################################################################################

def main():

    if RUN_EXTRACTED:

        print('\nANALYZING EXTRACTED EEG DATA...')

        ## LOAD DATA

        # Load extracted MIPDP data & relevant metadata
        data = np.load(FOLDER_EXTRACTED / 'data.npy')
        ages = np.load(FOLDER_EXTRACTED / 'ages.npy')

        ## APERIODIC MEASURES

        # Compute measures of interest on the data
        results = run_measures(data, MEASURES)
        save_pickle(results, 'eeg2_results', OUTPATH)

        ## APERIODIC CORRELATIONS

        # Compute correlations across all pairs of methods
        all_corrs = compute_all_corrs(results)
        save_pickle(all_corrs, 'eeg2_all_corrs', OUTPATH)

        ## PEAK MEASURES

        # Compute periodic measures
        peak_results = run_measures(data, PEAK_MEASURES)
        save_pickle(peak_results, 'eeg2_peak_results', OUTPATH)

        ## PEAK CORRELATIONS

        # Compute correlations between aperiodic measures and alpha power
        alpha_corrs = compute_corrs_to_feature(results, peak_results['alpha_power'])
        save_pickle(alpha_corrs, 'eeg2_alpha_corrs', OUTPATH)

        # Compute differences between correlations between aperiodic measures and alpha power
        alpha_corr_diffs = compute_diffs_to_feature(results, peak_results['alpha_power'])
        save_pickle(alpha_corr_diffs, 'eeg2_alpha_corr_diffs', OUTPATH)

        ## AGE CORRELATIONS

        # Compute the correlations between each measure and age
        age_corrs = compute_corrs_to_feature(results, ages)
        save_pickle(age_corrs, 'eeg2_age_corrs', OUTPATH)

        # Compute the differences between measure-to-age correlations
        age_corr_diffs = compute_diffs_to_feature(results, ages)
        save_pickle(age_corr_diffs, 'eeg2_age_corr_diffs', OUTPATH)

        print('COMPLETED EXTRACTED EEG DATA ANALYSES\n')

    ###############################################################################################

    if RUN_GROUP:

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
