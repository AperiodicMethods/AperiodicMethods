"""I/O utilities for loading empirical data."""

import csv

import numpy as np
import pandas as pd
from scipy.io import loadmat

import mne
from mne.io import read_raw_edf

from apm.io.io import check_folder
from apm.data.settings import EEG1, EEG2

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

def load_eeg_dev_info(data_path):
    """Helper function to load montage & info for dev EEG data."""

    # Read in list of channel names that are kept in reduced 111 montage
    with open(data_path / 'chans111.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        ch_labels = list(reader)[0]

    montage = mne.channels.make_standard_montage('GSN-HydroCel-129')
    info = mne.create_info(ch_labels, EEG2['fs'], 'eeg')
    info = info.set_montage(montage)

    return info


## IEEG DATA

def load_ieeg_file(file, folder, max_time=None, return_channels=False):
    """Helper function to load a file of iEEG data."""

    edf = read_raw_edf(folder / file, verbose=False)

    # Extract data attributes of interest from object
    times = edf.times
    data = np.array(edf.get_data())

    # Collect channel names, and strip 'W' marker
    ch_names = [ch[0:-1] for ch in edf.ch_names]

    # Restrict data to times of interest
    if max_time:
        mask = times < max_time
        data = data[:, mask]
        times = times[mask]

    times = times.astype('float32')
    data = data.astype('float32')

    if not return_channels:
        return times, data
    else:
        return times, data, ch_names


def load_ieeg_all(files, folder, max_time=None, exclude_files=None, return_channels=False):
    """Helper function to load all iEEG data together."""

    all_data = []
    all_chs = []
    for file in files:

        if exclude_files:
            if file in exclude_files:
                continue

        _, data, chs = load_ieeg_file(file, folder, max_time=max_time, return_channels=True)
        all_data.append(data)
        all_chs.extend(chs)

    all_data = np.vstack(all_data)

    if not return_channels:
        return all_data
    else:
        return all_data, all_chs


def load_ieeg_metadata(path):
    """Load metadata files for the iEEG dataset."""

    ch_info = pd.read_csv(path / 'ChannelInformation.csv', dtype = {'Channel name': str})
    ch_info['Channel name'] = [ch[1:-1] for ch in ch_info['Channel name']]

    patient_info = pd.read_csv(path / 'PatientInformation.csv')
    region_info = pd.read_csv(path / 'RegionInformation.csv')

    return ch_info, patient_info, region_info


def get_patient_info(chs, ch_info, patient_info):
    """Get patient information, based on a set of channel labels."""

    patients = [ch_info[ch_info['Channel name'] == ch]['Patient'].values[0] for ch in chs]
    ages = [patient_info[patient_info['ID'] == patient]['Age at time of study'].values[0] \
        for patient in patients]

    return np.array(patients), np.array(ages)
