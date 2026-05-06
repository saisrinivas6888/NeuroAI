import numpy as np
import mne

# Load epochs
epochs = mne.read_epochs("../data/processed/epochs/sub-001_epo.fif", preload=True)
print(epochs)

# Load connectivity matrix
m = np.load("../data/processed/connectivity/sub-001_conn.npy")

# Load raw EEG
raw = mne.io.read_raw_eeglab(
    "../data/raw/sub-001/eeg/sub-001_task-eyesclosed_eeg.set",
    preload=True
)

print("Sampling Rate:", raw.info['sfreq'])

print("Shape:", m.shape)
print("Contains NaN:", np.isnan(m).any())
print("Min:", m.min())
print("Max:", m.max())