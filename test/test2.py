import mne

epochs = mne.read_epochs("../data/processed/epochs/sub-002_epo.fif")

print("Sampling rate:", epochs.info['sfreq'])
print("Channels:", len(epochs.ch_names))
print("Channel names:", epochs.ch_names)
print("Epochs per subject:", len(epochs))