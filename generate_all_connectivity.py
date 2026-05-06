# generate_all_connectivity.py
import mne
from src.utils.labels import load_labels
from src.features.connectivity import save_subject_connectivity
from src.config import EPOCHS_DIR

labels = load_labels()

for subject_id in labels.keys():
    epo_path = EPOCHS_DIR / f"{subject_id}_epo.fif"
    if not epo_path.exists():
        print(f"Skipping {subject_id}: epochs not found")
        continue

    epochs = mne.read_epochs(epo_path, preload=True, verbose=False)
    save_subject_connectivity(subject_id, epochs)

print(" All connectivity matrices generated")