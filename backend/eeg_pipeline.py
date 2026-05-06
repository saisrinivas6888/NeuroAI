import mne
import numpy as np
from src.data.preprocess import preprocess_raw
from src.data.epoching import make_epochs
from src.features.connectivity import save_subject_connectivity


def process_uploaded_eeg(file_path, subject_id="web_subject"):
    
    # Load uploaded .set EEG file
    raw = mne.io.read_raw_eeglab(file_path, preload=True)

    # Apply your preprocessing (same as training)
    raw = preprocess_raw(raw)

    # Create epochs
    epochs = make_epochs(raw)

    # Generate connectivity using your original function
    conn = save_subject_connectivity(subject_id, epochs)

    return conn