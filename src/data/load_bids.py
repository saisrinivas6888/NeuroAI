# src/data/load_bids.py

import mne
from pathlib import Path
from src.config import RAW_DATA_DIR


def load_subject_raw(subject_id):
    """
    Load raw EEG for a subject from BIDS structure.
    Supports EDF / SET / BrainVision formats.
    """
    subject_path = RAW_DATA_DIR / subject_id

    if not subject_path.exists():
        raise FileNotFoundError(f"Subject folder not found: {subject_path}")

    # Supported EEG extensions
    eeg_exts = [".edf", ".set", ".vhdr"]

    eeg_files = []
    for ext in eeg_exts:
        eeg_files.extend(subject_path.rglob(f"*{ext}"))

    if len(eeg_files) == 0:
        raise FileNotFoundError(
            f"No EEG file found for {subject_id}. "
            f"Checked extensions: {eeg_exts}"
        )

    eeg_file = eeg_files[0]
    print(f"✔ Loading EEG file: {eeg_file.name}")

    # Load based on file type
    if eeg_file.suffix == ".edf":
        raw = mne.io.read_raw_edf(eeg_file, preload=True, verbose=False)
    elif eeg_file.suffix == ".set":
        raw = mne.io.read_raw_eeglab(eeg_file, preload=True, verbose=False)
    elif eeg_file.suffix == ".vhdr":
        raw = mne.io.read_raw_brainvision(eeg_file, preload=True, verbose=False)
    else:
        raise RuntimeError("Unsupported EEG file format")

    return raw