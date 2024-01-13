"""Analysis script for analyzing the demo EEG dataset."""

from pathlib import Path
from copy import deepcopy

import numpy as np

# Import custom code
import sys; from pathlib import Path
sys.path.append(str(Path('..').resolve()))
from apm.io import APMDB, get_files, save_pickle
from apm.io.data import load_eeg_demo_data, load_eeg_demo_group_data
from apm.data.measures import MEASURES, PEAK_MEASURES
from apm.analysis import (compute_avgs, compute_all_corrs,
                          compute_corrs_to_feature, compute_diffs_to_feature)
from apm.run import run_measures, run_group_measures

###################################################################################################
###################################################################################################

# Run settings
RUN_EXTRACTED = True
RUN_GROUP = True

# Define the data folders
FOLDER_EXTRACTED = Path('/Users/tom/Data/VoytekLab/ExtractedSubsets/eeg_data')
FOLDER_GROUP = Path('/Users/tom/Documents/Research/2-Projects/1a-Current(Voytek)/AperiodicMethods/2-Data/apm_data/')

# Settings for saving out results files
OUTPATH = APMDB().data_path / 'eeg1'

# Define data field to extract from files
DATA_FIELD = 'oz_rest_data'

###################################################################################################
###################################################################################################

def main():

    ##############################################################################################

    ## LOAD DATA

    if RUN_EXTRACTED:

        print('\nANALYZING EXTRACTED EEG DATA...')

        # Get the list of available files
        files = get_files(FOLDER_EXTRACTED, select='.mat')

        # FIX: temporarily drop subject which has a data quirk (wrong size array)
        files.remove('1009.mat')

        # Load data
        data = load_eeg_demo_data(files, FOLDER_EXTRACTED, DATA_FIELD)

        ## APERIODIC MEASURES

        # Compute measures of interest on the data
        results = run_measures(data, MEASURES)
        save_pickle(results, 'eeg1_results', OUTPATH)

        ## XX

        # Compute correlations across all pairs of methods
        all_corrs = compute_all_corrs(results)
        save_pickle(all_corrs, 'eeg1_all_corrs', OUTPATH)

        ## PEAK MEASURES

        # Compute periodic measures
        peak_results = run_measures(data, PEAK_MEASURES)
        save_pickle(peak_results, 'eeg1_peak_results', OUTPATH)

        ## PEAK CORRELATIONS
        alpha_corrs = compute_corrs_to_feature(results, peak_results['alpha_power'])
        save_pickle(alpha_corrs, 'eeg1_alpha_corrs', OUTPATH)

        alpha_corr_diffs = compute_diffs_to_feature(results, peak_results['alpha_power'])
        save_pickle(alpha_corrs, 'eeg1_alpha_corr_diffs', OUTPATH)

        print('COMPLETED EXTRACTED EEG DATA ANALYSES\n')

    ###############################################################################################

    if RUN_GROUP:

        print('\nANALYZING GROUP EEG DATA...')

        ## LOAD DATA

        # Load group data
        group_data = load_eeg_demo_group_data(FOLDER_GROUP)

        ## APERIODIC MEASURES
        group_results = run_group_measures(group_data, MEASURES)
        save_pickle(group_results, 'eeg1_group_results', OUTPATH)

        ## APERIODIC CORRELATIONS

        # Compute average and subselect time domain measures
        group_avg = compute_avgs(group_results)
        group_avg_ts = {ke : va for ke, va in group_avg.items() \
            if ke not in ['specparam', 'irasa']}

        # Compute and save group correlations
        group_corrs = compute_all_corrs(group_avg_ts)
        save_pickle(group_corrs, 'eeg1_group_corrs', OUTPATH)

        # Compute and save differences
        group_exp_corrs = compute_corrs_to_feature(group_avg_ts, group_avg['specparam'])
        save_pickle(group_exp_corrs, 'eeg1_group_exp_corrs', OUTPATH)

        ## PEAK MEASURES

        # Compute group level peak measures
        group_results_peaks = run_group_measures(group_data, PEAK_MEASURES)
        group_results_peaks['alpha_power'] = np.log10(group_results_peaks['alpha_power'])
        save_pickle(group_results_peaks, 'eeg1_group_results_peaks', OUTPATH)

        ## PEAK CORRELATIONS

        # Compute correlations between peak measures and time domain measures
        group_avg_peaks = compute_avgs(group_results_peaks)
        group_alpha_corrs = compute_corrs_to_feature(\
            group_avg_ts, group_avg_peaks['alpha_power'])
        save_pickle(group_alpha_corrs, 'eeg1_group_alpha_corrs', OUTPATH)

        # Compute differences between peak correlations
        group_alpha_corr_diffs = compute_diffs_to_feature(\
            group_avg_ts, group_avg_peaks['alpha_power'])
        save_pickle(group_alpha_corr_diffs, 'eeg1_group_alpha_corr_diffs', OUTPATH)

        print('COMPLETED GROUP EEG DATA ANALYSES\n')


if __name__ == "__main__":
    main()
