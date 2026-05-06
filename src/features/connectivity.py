# src/features/connectivity.py

import numpy as np
import mne
from pathlib import Path
from src.config import CONNECTIVITY_DIR


def compute_connectivity(epochs):
    """
    Compute Pearson correlation connectivity for each epoch.

    Parameters
    ----------
    epochs : mne.Epochs
        Shape: (n_epochs, n_channels, n_times)

    Returns
    -------
    conn_matrices : np.ndarray
        Shape: (n_epochs, n_channels, n_channels)
    """
    data = epochs.get_data()  # (E, C, T)
    n_epochs, n_channels, _ = data.shape

    conn_matrices = np.zeros((n_epochs, n_channels, n_channels))

    for i in range(n_epochs):
        # Correlation across channels (time as samples)
        conn = np.corrcoef(data[i])
        conn = np.nan_to_num(conn)  # safety
        conn_matrices[i] = conn

    return conn_matrices


def save_subject_connectivity(subject_id, epochs):
    """
    Compute and save connectivity matrices for one subject.
    """
    conn = compute_connectivity(epochs)

    save_path = CONNECTIVITY_DIR / f"{subject_id}_conn.npy"
    np.save(save_path, conn)

    print(f" Saved connectivity: {save_path}")
    print(f"  Shape: {conn.shape}")