# src/training/dataset_subjectwise.py
import numpy as np
import torch
from torch.utils.data import Dataset
from src.utils.labels import load_labels
from src.config import CONNECTIVITY_DIR


class SubjectWiseConnectivityDataset(Dataset):
    def __init__(self, subjects):
        """
        subjects: list of subject IDs
        """
        self.labels = load_labels()
        self.samples = []

        for sid in subjects:
            path = CONNECTIVITY_DIR / f"{sid}_conn.npy"
            conn = np.load(path)   # (E, C, C)
            y = self.labels[sid]

            for i in range(conn.shape[0]):
                self.samples.append((conn[i], y, sid))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        x, y, sid = self.samples[idx]
        x = torch.tensor(x, dtype=torch.float32).unsqueeze(0)
        y = torch.tensor(y, dtype=torch.long)
        return x, y, sid