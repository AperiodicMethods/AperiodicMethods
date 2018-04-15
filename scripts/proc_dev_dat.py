"""Process EEG data from the EEGDev dataset, saving out PSDs from resting EEG data."""

import os
import csv
import numpy as np
import mne

from slf.eeg import fit_fooof_lst, fit_fooof_3d, get_slopes
from slf.core.db import SLFDB
from slf.core.io import save_pickle

####################################################################################################
####################################################################################################

# ???
SKIP_SUBJS = ['A00054488', 'A00054866', 'A00055623', 'A00056716', 'A00056733']
#SKIP_SUBJS = []

####################################################################################################
####################################################################################################

def main():

    # Get project database objects, and list of available subjects
    db = SLFDB()
    subjs = db.check_subjs()
    done = db.get_fooof_subjs()

    for cur_subj in subjs:

        # Skip specified subjects
        if cur_subj in SKIP_SUBJS:
            print('\n\n\nSKIPPING SUBJECT: ', str(cur_subj), '\n\n\n')
            continue

        # Skip subject if PSD already calculated
        if cur_subj in done:
            print('\n\n\nSUBJECT ALREADY RUN: ', str(cur_subj), '\n\n\n')
            continue

        # Print status
        print('\n\n\nRUNNING SUBJECT: ', str(cur_subj), '\n\n\n')

        # Get subject data files
        try:
            dat_f, ev_f, _ = db.get_subj_files(cur_subj)
            if dat_f is None:
                print('\n\n\nSKIPPING DUE TO FILE ISSUE: ', str(cur_subj), '\n\n\n')
                continue
        except:
            print('\tFAILED TO GET SUBJ FILES')
            continue

        # Get the resting data file - file 001
        temp = [ef.split('_')[1] for ef in ev_f]
        temp = [fn[-3:] for fn in temp]
        f_ind = None
        for i, tt in enumerate(temp):
            if tt == '001':
                f_ind = i
        if f_ind is None:
            print('\tFAILED TO FIND 001 BLOCK')
            continue

        # Get file file path for data file & associated event file
        dat_f_name = db.gen_dat_path(cur_subj, dat_f[f_ind])
        eve_f_name = db.gen_dat_path(cur_subj, ev_f[f_ind])

        # Set the sampling rate
        s_freq = 500

        # Load data file
        dat = np.loadtxt(dat_f_name, delimiter=',')

        # Read in list of channel names that are kept in reduced 111 montage
        with open('../data/chans111.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            ch_labels = list(reader)[0]

        # Read montage, reduced to 111 channel selection
        montage = mne.channels.read_montage('GSN-HydroCel-129', ch_names=ch_labels)

        # Create the info structure needed by MNE
        info = mne.create_info(ch_labels, s_freq, 'eeg', montage)

        # Create the MNE Raw data object
        raw = mne.io.RawArray(dat, info)

        # Create a stim channel
        stim_info = mne.create_info(['stim'], s_freq, 'stim')
        stim_raw = mne.io.RawArray(np.zeros(shape=[1, len(raw._times)]), stim_info)

        # Add stim channel to data object
        raw.add_channels([stim_raw], force_update_info=True)

        # Load events from file
        # Initialize headers and variable to store event info
        headers = ['type', 'value', 'latency', 'duration', 'urevent']
        evs = np.empty(shape=[0, 3])

        # Load events from csv file
        with open(eve_f_name, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:

                # Skip the empty rows
                if row == []:
                    continue

                # Skip the header row, since there is one for every event...
                if row[0] == 'type':
                    continue

                # Collect actual event data rows
                evs = np.vstack((evs, np.array([int(row[2]), 0, int(row[0])])))

        # Add events to data object
        raw.add_events(evs, stim_channel='stim')

        # Check events
        dat_evs = mne.find_events(raw)

        # Find flat channels and set them as bad
        flat_chans = np.mean(raw._data[:111, :], axis=1) == 0
        raw.info['bads'] = list(np.array(raw.ch_names[:111])[flat_chans])
        print('Bad channels: ', raw.info['bads'])

        # Interpolate bad channels
        raw.interpolate_bads()

        # Set average reference
        raw.set_eeg_reference()
        raw.apply_proj()

        # Get good eeg channel indices
        eeg_chans = mne.pick_types(raw.info, meg=False, eeg=True)

        # Epoch resting eeg data events
        eo_epochs = mne.Epochs(raw, events=dat_evs, event_id={'EO': 20}, tmin=2, tmax=18,
                               baseline=None, picks=eeg_chans, preload=True)
        ec_epochs = mne.Epochs(raw, events=dat_evs, event_id={'EC': 30}, tmin=5, tmax= 35,
                               baseline=None, picks=eeg_chans, preload=True)

        # Calculate PSDs - EO Data
        eo_psds, eo_freqs = mne.time_frequency.psd_welch(eo_epochs, fmin=2., fmax=40., n_fft=1000,
                                                         n_overlap=250, verbose=False)

        # Average PSDs for each channel across each rest block
        eo_avg_psds = np.mean(eo_psds, axis=0)

        # Calculate PSDs - EC Data
        ec_psds, ec_freqs = mne.time_frequency.psd_welch(ec_epochs, fmin=2., fmax=40., n_fft=1000,
                                                         n_overlap=250, verbose=False)

        # Average PSDs for each channel across each rest block
        ec_avg_psds = np.mean(ec_psds, axis=0)

        # Save out PSDs
        np.savez(os.path.join(db.psd_path, str(cur_subj) + '_ec_avg_psds.npz'),
                 ec_freqs, ec_avg_psds, np.array(ec_epochs.ch_names))
        np.savez(os.path.join(db.psd_path, str(cur_subj) + '_eo_avg_psds.npz'),
                 eo_freqs, eo_avg_psds, np.array(eo_epochs.ch_names))
        np.savez(os.path.join(db.psd_path, str(cur_subj) + '_ec_psds.npz'),
                 ec_freqs, ec_psds, np.array(ec_epochs.ch_names))
        np.savez(os.path.join(db.psd_path, str(cur_subj) + '_eo_psds.npz'),
                 eo_freqs, eo_psds, np.array(eo_epochs.ch_names))

        # Print status
        print('\n\n\nPSD DATA SAVED FOR SUBJ: ', str(cur_subj), '\n\n\n')
        print('\n\n\nFOOOFING DATA FOR SUBJ: ', str(cur_subj), '\n\n\n')

        # Fit FOOOF to PSDs averaged across rest epochs
        fres_eo_avg = fit_fooof_lst(eo_freqs, eo_avg_psds)
        sls_eo_avg = get_slopes(fres_eo_avg)
        fres_ec_avg = fit_fooof_lst(ec_freqs, ec_avg_psds)
        sls_ec_avg = get_slopes(fres_ec_avg)

        # Fit FOOOF to PSDs from each epoch
        fres_eo = fit_fooof_3d(eo_freqs, eo_psds)
        sls_eo = [get_slopes(lst) for lst in fres_eo]
        fres_ec = fit_fooof_3d(ec_freqs, ec_psds)
        sls_ec = [get_slopes(lst) for lst in fres_ec]

        # Collect data together
        subj_dat = {
            'ID' : cur_subj,
            'sls_eo_avg' : sls_eo_avg,
            'sls_ec_avg' : sls_ec_avg,
            'sls_eo' : sls_eo,
            'sls_ec' : sls_ec
        }

        # Save out FOOOF data
        f_name = str(cur_subj) + '_fooof.p'
        save_pickle(subj_dat, f_name, db.fooof_path)

        # Print status
        print('\n\n\nFOOOF DATA SAVED AND FINISHED WITH SUBJ: ', str(cur_subj), '\n\n\n')


if __name__ == "__main__":
    main()
