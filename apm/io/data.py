"""I/O utilities for loading empirical data."""

import numpy as np
from scipy.io import loadmat

import mne
from mne.io import read_raw_edf

from apm.io.io import check_folder
from apm.data.settings import EEG1

###################################################################################################
###################################################################################################

## EEG1: DEMO DATA
def load_eeg_demo_data(files, folder, data_field):
    """Helper function for loading the EEG demo dataset."""

    data = []
    for file in files:
        loaded = loadmat(check_folder(file, folder), squeeze_me=True)
        data.append(loaded[data_field])
    data = np.array(data)

    return data


def load_eeg_demo_group_data(data_path):
    """Helper function to load complete group of demo EEG data."""

    data1 = np.load(data_path / 'rtPB_extracted_block.npy')
    data2 = np.load(data_path / 'PBA_extracted_block.npy')
    group_data = np.vstack([data1, data2])

    return group_data


def load_eeg_demo_info(data_path):
    """Helper function to load montage & info for demo EEG data."""

    with open(data_path / 'ch_names.txt') as file:
        ch_names = [str(line.strip()) for line in file]

    montage = mne.channels.make_standard_montage('standard_1020')
    info = mne.create_info(ch_names, EEG1['fs'], 'eeg')
    info = info.set_montage(montage)

    return info

## EEG2: DEV DATA

...

## IEEG DATA

def load_ieeg_file(file, folder, max_time=None):
    """Helper function to load a file of iEEG data."""

    edf = read_raw_edf(folder / file, verbose=False)

    # Extract times series from data object
    times = edf.times
    data = np.array(edf.get_data())

    # Restrict data to times of interest
    if max_time:
        mask = times < max_time
        data = data[:, mask]
        times = times[mask]

    times = times.astype('float32')
    data = data.astype('float32')

    return times, data


def load_ieeg_all(files, folder, max_time=None):
    """Helper function to load all iEEG data together."""

    all_data = []
    for file in files:

        _, data = load_ieeg_file(file, folder, max_time=max_time)
        all_data.append(data)

    all_data = np.vstack(all_data)

    return all_data
