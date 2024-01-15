"""Analysis script for analyzing the MNI iEEG dataset."""

from pathlib import Path

from mne.io import read_raw_edf

# Import custom code
import sys
sys.path.append(str(Path('..').resolve()))
from apm.io.data import load_ieeg_all
from apm.io import APMDB, get_files, save_pickle
from apm.analysis import compute_all_corrs
from apm.data.measures import MEASURES_LONG as MEASURES
from apm.run import run_measures

###################################################################################################
###################################################################################################

# Define max time to load
MAX_TIME = 30

# Define the data folder
DATA_FOLDER = Path('/Users/tom/Data/External/iEEG/MNI/Wakefulness_AllRegions/')

# Settings for saving out results files
OUTPATH = APMDB().data_path / 'ieeg'

###################################################################################################
###################################################################################################

def main():

    print('\nANALYZING IEEG DATA...')

    ## LOAD DATA

    # Get the list of available files
    files = get_files(DATA_FOLDER)

    # Load all ieeg data files
    all_data = load_ieeg_all(files, DATA_FOLDER, MAX_TIME)

    ## APERIODIC MEASURES

    # Compute measures of interest on the iEEG data
    results = run_measures(all_data, MEASURES)
    save_pickle(results, 'ieeg_results', OUTPATH)

    ## APERIODIC CORRELATIONS

    # Compute correlations across all pairs of methods
    all_corrs = compute_all_corrs(results)
    save_pickle(all_corrs, 'ieeg_all_corrs', OUTPATH)

    print('COMPLETED IEEG DATA ANALYSES\n')


if __name__ == "__main__":
    main()
