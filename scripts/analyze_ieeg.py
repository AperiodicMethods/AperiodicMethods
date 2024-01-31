"""Analysis script for analyzing the MNI iEEG dataset."""

from pathlib import Path

import numpy as np

from fooof import FOOOFGroup
from fooof.utils.params import compute_knee_frequency
from neurodsp.spectral import compute_spectrum

# Import custom code
import sys
sys.path.append(str(Path('..').resolve()))
from apm.io.data import load_ieeg_all
from apm.io import APMDB, get_files, save_pickle
from apm.run import run_measures
from apm.analysis import compute_all_corrs
from apm.data.measures import TS_MEASURES, SPECPARAM_SETTINGS_KNEE

from apm.methods import irasa

###################################################################################################
###################################################################################################

## PATH SETTINGS

# Define the data folder
DATA_FOLDER = Path('/Users/tom/Data/External/iEEG/MNI/Wakefulness_AllRegions/')

# Settings for saving out results files
OUTPATH = APMDB().data_path / 'ieeg'

# Define set of non-cortical areas
NON_CORTICAL = [
    'Amygdala_W.edf',
    'Anterior cingulate_W.edf',
    'Anterior insula_W.edf',
    'Fusiform and parahippocampal gyri_W.edf',
    'Hippocampus_W.edf',
    'Middle cingulate_W.edf',
    'Posterior cingulate_W.edf',
    'Posterior insula_W.edf',
]

## DATA PROPERTIES

# Define sampling frequency of current dataset
FS = 200

# Define max time to load
MAX_TIME = 30

## METHOD SETTINGS

#FIT_RANGE = [1, 75]
FIT_RANGE = [1, 60]

PSD_SETTINGS = {
    'fs' : FS,
    'nperseg' : 2 * FS,
    'noverlap' : FS,
}

IRASA_SETTINGS = {
    'fs' : FS,
    'f_range' : FIT_RANGE,
    'fit_func' : 'fit_irasa_knee',
}

IRASA_MEASURES = {
    irasa : IRASA_SETTINGS,
}

MEASURES = TS_MEASURES | IRASA_MEASURES

###################################################################################################
###################################################################################################

def main():

    print('\nANALYZING IEEG DATA...')

    ## LOAD DATA

    # Get the list of available files
    files = get_files(DATA_FOLDER)

    # Load all ieeg data files
    all_data = load_ieeg_all(files, DATA_FOLDER, MAX_TIME, exclude_files=NON_CORTICAL)

    ## APERIODIC MEASURES

    # Compute measures of interest on the iEEG data
    results = run_measures(all_data, MEASURES)

    # Run specparam
    freqs, powers = compute_spectrum(all_data, **PSD_SETTINGS)
    fg = FOOOFGroup(**SPECPARAM_SETTINGS_KNEE)
    fg.fit(freqs, powers, FIT_RANGE)
    fg.save('ieeg_specparam', OUTPATH, save_results=True)

    # Add specparam measures to overall results
    results['specparam'] = np.array(fg.get_params('aperiodic', 'exponent'))
    knee_freqs = [compute_knee_frequency(kn, exp) \
        for kn, exp in zip(fg.get_params('aperiodic', 'knee'),
                           fg.get_params('aperiodic', 'exponent'))]
    results['specparam_knee'] = np.array(fg.get_params('aperiodic', 'knee'))
    results['specparam_knee_freq'] = np.nan_to_num(np.array(knee_freqs))

    save_pickle(results, 'ieeg_results', OUTPATH)

    ## APERIODIC CORRELATIONS

    # Compute correlations across all pairs of methods
    all_corrs = compute_all_corrs(results)
    save_pickle(all_corrs, 'ieeg_all_corrs', OUTPATH)

    print('COMPLETED IEEG DATA ANALYSES\n')


if __name__ == "__main__":
    main()
