# generate_all_epochs.py

import mne
from src.utils.labels import load_labels
from src.data.load_bids import load_subject_raw
from src.data.preprocess import preprocess_raw
from src.data.epoching import make_epochs
from src.config import EPOCHS_DIR

labels = load_labels()

for subject_id in labels.keys():
    save_path = EPOCHS_DIR / f"{subject_id}_epo.fif"

    if save_path.exists():
        print(f"Skipping {subject_id}: epochs already exist")
        continue

    try:
        raw = load_subject_raw(subject_id)
        raw = preprocess_raw(raw)
        epochs = make_epochs(raw)
        epochs.save(save_path, overwrite=True)
        print(f"✔ Saved epochs for {subject_id}")
    except Exception as e:
        print(f"Failed for {subject_id}: {e}")

print(" Epoch generation complete")