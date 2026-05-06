# src/data/epoching.py

import mne
from src.config import EPOCH_LENGTH, OVERLAP


def make_epochs(raw):
    """
    Create fixed-length epochs
    """
    events = mne.make_fixed_length_events(
        raw,
        start=0,
        duration=EPOCH_LENGTH,
        overlap=EPOCH_LENGTH * OVERLAP
    )

    epochs = mne.Epochs(
        raw,
        events,
        tmin=0,
        tmax=EPOCH_LENGTH,
        baseline=None,
        preload=True,
        verbose=False
    )

    return epochs