"""Analysis script for analyzing the demo EEG dataset."""

from pathlib import Path

# Import custom code
import sys
sys.path.append(str(Path('..').resolve()))
from apm.io import APMDB, save_pickle
from apm.io.data import load_eeg_demo_group_data
from apm.data.measures import MEASURES, PEAK_MEASURES
from apm.analysis import compute_avgs, compute_all_corrs, compute_corrs_to_feature
from apm.run import run_measures, run_group_measures

###################################################################################################
###################################################################################################

# Define data folder
FOLDER = Path('/Users/tom/Documents/Research/2-Projects/1a-Current(Voytek)/AperiodicMethods/2-Data/apm_data/')

# Settings for saving out results files
OUTPATH = APMDB().data_path / 'eeg1'

# Define data field to extract from files
DATA_FIELD = 'oz_rest_data'

###################################################################################################
###################################################################################################

def main():

    print('\nANALYZING GROUP EEG DATA...')

    ## LOAD DATA

    # Load group data
    group_data = load_eeg_demo_group_data(FOLDER)

    ## APERIODIC MEASURES

    group_results = run_group_measures(group_data, MEASURES)
    save_pickle(group_results, 'eeg1_group_results', OUTPATH)

    ## PEAK MEASURES

    # Compute group level peak measures
    group_results_peaks = run_group_measures(group_data, PEAK_MEASURES)
    save_pickle(group_results_peaks, 'eeg1_group_results_peaks', OUTPATH)

    ## APERIODIC CORRELATIONS

    # Compute average and sub-select time domain measures
    group_avg = compute_avgs(group_results)
    group_avg_ts = {ke : va for ke, va in group_avg.items() \
        if ke not in ['specparam', 'irasa']}

    # Compute and save spatial correlations across time domain measures
    group_corrs = compute_all_corrs(group_avg_ts)
    save_pickle(group_corrs, 'eeg1_spatial_corrs', OUTPATH)

    # Compute and save spatial correlations between time domain and exponent measures
    group_exp_corrs = compute_corrs_to_feature(group_avg_ts, group_avg['specparam'])
    save_pickle(group_exp_corrs, 'eeg1_spatial_corrs_exp', OUTPATH)

    ## PEAK CORRELATIONS

    # Compute spatial correlations between peak measures and time domain measures
    group_avg_peaks = compute_avgs(group_results_peaks)
    group_alpha_corrs = compute_corrs_to_feature(\
        group_avg_ts, group_avg_peaks['alpha_power'])
    save_pickle(group_alpha_corrs, 'eeg1_spatial_corrs_alpha', OUTPATH)

    # # Compute differences between peak correlations
    # group_alpha_corr_diffs = compute_diffs_to_feature(\
    #     group_avg_ts, group_avg_peaks['alpha_power'])
    # save_pickle(group_alpha_corr_diffs, 'eeg1_group_alpha_corr_diffs', OUTPATH)

    print('COMPLETED GROUP EEG DATA ANALYSES\n')


if __name__ == "__main__":
    main()
