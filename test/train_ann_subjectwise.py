import numpy as np
import torch
import torch.nn as nn
from pathlib import Path

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
# Paths
# =====================
SAVE_DIR = Path("results/metrics/ann_subjectwise")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


# =====================
# Load data
# =====================
labels = load_labels()
subjects = list(labels.keys())

X, y = [], []

for sid in subjects:
    conn = load_subject_connectivity(sid)   # (epochs, 19, 19)
    conn_mean = conn.mean(axis=0)           # (19, 19)
    X.append(conn_mean.flatten())           # (361,)
    y.append(labels[sid])

X = torch.tensor(np.array(X), dtype=torch.float32)
y = np.array(y)


# =====================
# ANN model definition
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


# =====================
# 5-Fold Subject-wise CV
# =====================
skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

fold_metrics = []

for fold, (train_idx, test_idx) in enumerate(skf.split(X, y), 1):

    model = ANN()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    X_train = X[train_idx]
    y_train = torch.tensor(y[train_idx], dtype=torch.long)

    X_test = X[test_idx]
    y_test = y[test_idx]

    # ---- Train ----
    model.train()
    for _ in range(30):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

    # ---- Evaluate ----
    model.eval()
    with torch.no_grad():
        logits = model(X_test)
        probs = torch.softmax(logits, dim=1)[:, 1].numpy()
        preds = (probs > 0.5).astype(int)

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1": f1_score(y_test, preds),
        "roc_auc": roc_auc_score(y_test, probs)
    }

    print(
        f"Fold {fold} → "
        f"Acc: {metrics['accuracy']:.3f}, "
        f"F1: {metrics['f1']:.3f}, "
        f"AUC: {metrics['roc_auc']:.3f}"
    )

    fold_metrics.append(metrics)


# =====================
# Save results
# =====================
np.save(SAVE_DIR / "fold_metrics.npy", fold_metrics)

# =====================
# Mean results
# =====================
print("\n📊 ANN SUBJECT-WISE (5-FOLD CV)")
for key in fold_metrics[0].keys():
    mean_val = np.mean([m[key] for m in fold_metrics])
    print(f"{key.capitalize():<10}: {mean_val:.3f}")