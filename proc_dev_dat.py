"""   """

import csv
import numpy as np
import mne


from slf.core.db import SLFDB


##
##

def main():

    # Get project database objects, and list of available subjects
    db = SLFDB()
    subjs = db.check_subjs()

    for cur_subj in subjs:

        # Print sats
        print('\n\n\nRUNNING SUBJECT: ', str(cur_subj), '\n\n\n')

        # Get subject data files
        try:
            dat_f, ev_f, _ = db.get_subj_files(cur_subj)
        except:
            continue

        # Get the resting data file - file 001
        temp = [ef.split('_')[1] for ef in ev_f]
        temp = [fn[-3:] for fn in temp]
        f_ind = None
        for i in range(len(temp)):
            if temp[i] == '001':
                f_ind = i
        if not f_ind:
            continue

        # Get file file path for data file & associated event file
        dat_f_name = db.gen_dat_path(cur_subj, dat_f[f_ind])
        eve_f_name = db.gen_dat_path(cur_subj, ev_f[f_ind])

        # Load data file
        dat = np.loadtxt(dat_f_name, delimiter=',')

        # Read default montage
        montage = mne.channels.read_montage('GSN-HydroCel-129')
        keep_chans = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20,
                      21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                      38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 57,
                      58, 59, 60, 61, 62, 64, 65, 66, 67, 69, 70, 71, 72, 74, 75, 76, 77,
                      78, 79, 80, 82, 83, 84, 85, 86, 87, 89, 90, 91, 92, 93, 95, 96, 97,
                      98, 100, 101, 102, 103, 104, 105, 106, 108, 109, 110, 111, 112, 114,
                      115, 116, 117, 118, 120, 121, 122, 123, 124, 129])

        # Fix zero based indexing (screw off matlab)
        keep_chans = keep_chans - 1

        # Get channel names to keep
        kept_chans = list(np.array(montage.ch_names)[keep_chans])

        # Settings for loading data
        s_freq = 500

        # Create the info structure needed by MNE
        info = mne.create_info(kept_chans, s_freq, 'eeg')

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
                if row == []: continue

                # Skip the header row, since there is one FOR EVERY DAMN EVENT. SERIOUSLY?
                if row[0] == 'type': continue

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

        # Get good eeg channel indices
        eeg_chans = mne.pick_types(raw.info, meg=False, eeg=True)

        # Epoch resting eeg data events
        eo_epochs = mne.Epochs(raw, events=dat_evs, event_id={'EO': 20},
                               tmin=5, tmax=15, baseline=None, picks=eeg_chans,
                               add_eeg_ref=False, preload=True)
        ec_epochs = mne.Epochs(raw, events=dat_evs, event_id={'EC': 30},
                               tmin=5, tmax= 35, baseline=None, picks=eeg_chans,
                               add_eeg_ref=False, preload=True)

        # Calculate PSDs - EO Data
        eo_psds, eo_freqs = mne.time_frequency.psd_welch(eo_epochs, fmin=1.,
                                                         fmax=40., n_fft=1000)

        # Average PSDs for each channel across each rest block
        eo_avg_psds = np.mean(eo_psds, axis=0)

        # Calculate PSDs - EC Data
        ec_psds, ec_freqs = mne.time_frequency.psd_welch(ec_epochs, fmin=3.,
                                                         fmax=40., n_fft=1000)

        # Average PSDs for each channel across each rest block
        ec_avg_psds = np.mean(ec_psds, axis=0)

        # Save out PSDs
        np.savez(str(cur_subj) + 'ec_psds.npz', ec_freqs, ec_avg_psds,
                 np.array(ec_epochs.ch_names))
        np.savez(str(cur_subj) + 'eo_psds.npz', eo_freqs, eo_avg_psds,
                 np.array(eo_epochs.ch_names))

        # Print status
        print('\n\n\nSAVED DATA FOR SUBJ: ', str(cur_subj), '\n\n\n')


if __name__ == "__main__":
    main()
