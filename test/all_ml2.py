import numpy as np
import torch
import torch.nn as nn
from pathlib import Path
import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from src.utils.labels import load_labels
from src.utils.connectivity_loader import load_subject_connectivity


# =====================
# Config
# =====================
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
N_FOLDS = 5
EPOCHS = 20
LR = 1e-3
SEED = 42

torch.manual_seed(SEED)
np.random.seed(SEED)

SAVE_DIR = Path("results/metrics/deep_baselines")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


# =====================
# Load subject-level data
# =====================
labels = load_labels()
subjects = list(labels.keys())

X_ann, X_seq, y = [], [], []

for sid in subjects:
    conn = load_subject_connectivity(sid)      # (epochs, 19, 19)
    conn_mean = conn.mean(axis=0)               # (19, 19)

    X_ann.append(conn_mean.flatten())           # (361,)
    X_seq.append(conn_mean)                     # (19, 19)
    y.append(labels[sid])

X_ann = np.array(X_ann)
X_seq = np.array(X_seq)
y = np.array(y)


# =====================
# Models
# =====================
class ANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(361, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 2)
        )

    def forward(self, x):
        return self.net(x)


class RNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.rnn = nn.RNN(19, 32, batch_first=True)
        self.fc = nn.Linear(32, 2)

    def forward(self, x):
        _, h = self.rnn(x)
        return self.fc(h.squeeze(0))


class BiLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(19, 32, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(64, 2)

    def forward(self, x):
        _, (h, _) = self.lstm(x)
        h = torch.cat((h[-2], h[-1]), dim=1)
        return self.fc(h)


class ShallowCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.fc = nn.Linear(8, 2)

    def forward(self, x):
        x = x.unsqueeze(1)   # (B, 1, 19, 19)
        x = self.conv(x)
        return self.fc(x.view(x.size(0), -1))


models = {
    "ANN": (ANN, "ann"),
    "RNN": (RNNModel, "seq"),
    "BiLSTM": (BiLSTM, "seq"),
    "CNN": (ShallowCNN, "seq")
}


# =====================
# 5-Fold Subject-wise CV
# =====================
skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
results = []

for name, (model_class, mode) in models.items():
    print(f"\nRunning {name}...")
    fold_metrics = []

    for train_idx, test_idx in skf.split(X_ann, y):

        model = model_class().to(DEVICE)
        optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        criterion = nn.CrossEntropyLoss()

        if mode == "ann":
            Xtr = torch.tensor(X_ann[train_idx], dtype=torch.float32).to(DEVICE)
            Xte = torch.tensor(X_ann[test_idx], dtype=torch.float32).to(DEVICE)
        else:
            Xtr = torch.tensor(X_seq[train_idx], dtype=torch.float32).to(DEVICE)
            Xte = torch.tensor(X_seq[test_idx], dtype=torch.float32).to(DEVICE)

        ytr = torch.tensor(y[train_idx], dtype=torch.long).to(DEVICE)
        yte = y[test_idx]

        # ---- Train
        model.train()
        for _ in range(EPOCHS):
            optimizer.zero_grad()
            loss = criterion(model(Xtr), ytr)
            loss.backward()
            optimizer.step()

        # ---- Evaluate
        model.eval()
        with torch.no_grad():
            probs = torch.softmax(model(Xte), dim=1)[:, 1].cpu().numpy()
            preds = (probs >= 0.5).astype(int)

        fold_metrics.append([
            accuracy_score(yte, preds),
            precision_score(yte, preds, zero_division=0),
            recall_score(yte, preds, zero_division=0),
            f1_score(yte, preds, zero_division=0),
            roc_auc_score(yte, probs)
        ])

    results.append([name, *np.mean(fold_metrics, axis=0)])


# =====================
# Save results
# =====================
df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
)

df.to_csv(SAVE_DIR / "deep_baseline_comparison.csv", index=False)

print("\n📊 DEEP LEARNING BASELINES (SUBJECT-WISE)")
print(df)
print(f"\nSaved to {SAVE_DIR / 'deep_baseline_comparison.csv'}")