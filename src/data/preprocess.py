# src/data/preprocess.py

import mne
from src.config import LOW_FREQ, HIGH_FREQ


def preprocess_raw(raw):
    """
    Basic EEG preprocessing
    """
    raw.filter(LOW_FREQ, HIGH_FREQ, fir_design="firwin")
    raw.set_eeg_reference("average", projection=True)
    raw.apply_proj()

    return raw