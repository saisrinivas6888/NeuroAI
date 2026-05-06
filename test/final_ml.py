import numpy as np
import pandas as pd
from pathlib import Path
import torch
import torch.nn as nn

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from src.utils.labels import load_labels
from src.utils.connectivity_loader import load_subject_connectivity
from src.models.cnn_attention import CNNAttention


# =====================
# Config
# =====================
SEED = 42
N_FOLDS = 5
EPOCHS = 15        # FAST
LR = 1e-3
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

np.random.seed(SEED)
torch.manual_seed(SEED)

SAVE_DIR = Path("results/metrics/final_baselines")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


# =====================
# Load subject-level data
# =====================
labels = load_labels()
subjects = list(labels.keys())

X_img, X_vec, X_seq, y = [], [], [], []

for sid in subjects:
    conn = load_subject_connectivity(sid)
    conn_mean = conn.mean(axis=0)          # (19, 19)

    X_img.append(conn_mean[None, :, :])    # CNN input: (1, 19, 19)
    X_vec.append(conn_mean.flatten())      # SVM / Tree
    X_seq.append(conn_mean)                # RNN
    y.append(labels[sid])

X_img = torch.tensor(np.array(X_img), dtype=torch.float32)
X_vec = np.array(X_vec)
X_seq = np.array(X_seq)
y = np.array(y)


# =====================
# RNN model (UNCHANGED)
# =====================
class RNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.rnn = nn.RNN(19, 32, batch_first=True)
        self.fc = nn.Linear(32, 2)

    def forward(self, x):
        _, h = self.rnn(x)
        return self.fc(h.squeeze(0))


# =====================
# Classical baselines
# =====================
baselines = {
    "LinearSVM": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", SVC(
            kernel="linear",
            probability=True,
            class_weight="balanced",
            random_state=SEED
        ))
    ]),
    "DecisionTree": DecisionTreeClassifier(
        max_depth=4,
        class_weight="balanced",
        random_state=SEED
    )
}


# =====================
# Cross-validation
# =====================
skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
results = []


# =====================
# Run classical baselines
# =====================
for name, model in baselines.items():
    fold_scores = []

    for train_idx, test_idx in skf.split(X_vec, y):
        model.fit(X_vec[train_idx], y[train_idx])

        y_pred = model.predict(X_vec[test_idx])
        y_score = model.predict_proba(X_vec[test_idx])[:, 1]

        fold_scores.append([
            accuracy_score(y[test_idx], y_pred),
            precision_score(y[test_idx], y_pred, zero_division=0),
            recall_score(y[test_idx], y_pred, zero_division=0),
            f1_score(y[test_idx], y_pred, zero_division=0),
            roc_auc_score(y[test_idx], y_score)
        ])

    results.append([name, *np.mean(fold_scores, axis=0)])


# =====================
# Run RNN baseline
# =====================
fold_scores = []

for train_idx, test_idx in skf.split(X_seq, y):
    model = RNNModel().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss()

    Xtr = torch.tensor(X_seq[train_idx], dtype=torch.float32).to(DEVICE)
    ytr = torch.tensor(y[train_idx], dtype=torch.long).to(DEVICE)
    Xte = torch.tensor(X_seq[test_idx], dtype=torch.float32).to(DEVICE)
    yte = y[test_idx]

    for _ in range(EPOCHS):
        optimizer.zero_grad()
        loss = criterion(model(Xtr), ytr)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        probs = torch.softmax(model(Xte), dim=1)[:, 1].cpu().numpy()
        preds = (probs >= 0.5).astype(int)

    fold_scores.append([
        accuracy_score(yte, preds),
        precision_score(yte, preds, zero_division=0),
        recall_score(yte, preds, zero_division=0),
        f1_score(yte, preds, zero_division=0),
        roc_auc_score(yte, probs)
    ])

results.append(["RNN", *np.mean(fold_scores, axis=0)])


# =====================
# Run CNN + Attention (FAST BASELINE)
# =====================
fold_scores = []

for train_idx, test_idx in skf.split(X_img, y):
    model = CNNAttention().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss()

    Xtr = X_img[train_idx].to(DEVICE)
    ytr = torch.tensor(y[train_idx], dtype=torch.long).to(DEVICE)
    Xte = X_img[test_idx].to(DEVICE)
    yte = y[test_idx]

    for _ in range(EPOCHS):
        optimizer.zero_grad()
        loss = criterion(model(Xtr), ytr)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        probs = torch.softmax(model(Xte), dim=1)[:, 1].cpu().numpy()
        preds = (probs >= 0.5).astype(int)

    fold_scores.append([
        accuracy_score(yte, preds),
        precision_score(yte, preds, zero_division=0),
        recall_score(yte, preds, zero_division=0),
        f1_score(yte, preds, zero_division=0),
        roc_auc_score(yte, probs)
    ])

results.append(["CNN+Attention", *np.mean(fold_scores, axis=0)])


# =====================
# Save results
# =====================
df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
)

df.to_csv(SAVE_DIR / "baseline_comparison_fast_cnn_attention.csv", index=False)

print("\n FINAL BASELINE RESULTS (FAST, SUBJECT-WISE)")
print(df)
print(f"\nSaved to {SAVE_DIR / 'baseline_comparison_fast_cnn_attention.csv'}")