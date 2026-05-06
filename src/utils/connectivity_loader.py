import numpy as np
from pathlib import Path

DATA_DIR = Path("data/processed/connectivity")

def load_subject_connectivity(subject_id):
    """
    Load subject-wise connectivity data.

    Returns
    -------
    conn : np.ndarray
        Shape (epochs, 19, 19)
    """
    file_path = DATA_DIR / f"{subject_id}_conn.npy"
    return np.load(file_path)