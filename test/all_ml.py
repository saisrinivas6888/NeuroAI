import numpy as np
import torch
import torch.nn as nn
from pathlib import Path
import pandas as pd

from sklearn.model_selection import KFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from src.utils.labels import load_labels


# =====================
# Config
# =====================
DEVICE = "cpu"
N_FOLDS = 5
EPOCHS = 15
LR = 1e-3
SEED = 42

torch.manual_seed(SEED)
np.random.seed(SEED)

CONNECTIVITY_DIR = Path("data/processed/connectivity")
RESULT_DIR = Path("result/baselines")
RESULT_DIR.mkdir(parents=True, exist_ok=True)


# =====================
# Load connectivity
# =====================
def load_subject_connectivity(subject_id):
    return np.load(CONNECTIVITY_DIR / f"{subject_id}_conn.npy")


# =====================
# Models
# =====================
class ANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(361, 64),
            nn.ReLU(),
            nn.Dropout(0.6),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)


class RNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.rnn = nn.RNN(
            input_size=19,
            hidden_size=32,
            batch_first=True
        )
        self.fc = nn.Linear(32, 2)

    def forward(self, x):
        _, h = self.rnn(x)
        return self.fc(h.squeeze(0))


class BiLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=19,
            hidden_size=32,
            bidirectional=True,
            batch_first=True
        )
        self.fc = nn.Linear(64, 2)

    def forward(self, x):
        _, (h, _) = self.lstm(x)
        h = torch.cat((h[-2], h[-1]), dim=1)
        return self.fc(h)


# =====================
# Train & Evaluate
# =====================
def run_model(model_class, model_name):
    labels = load_labels()
    subjects = list(labels.keys())

    kf = KFold(
        n_splits=N_FOLDS,
        shuffle=True,
        random_state=SEED
    )

    fold_results = []

    for fold, (train_idx, test_idx) in enumerate(kf.split(subjects), 1):

        Xtr, ytr = [], []
        Xte, yte, sid_te = [], [], []

        # ---- Training data (epoch-wise)
        for i in train_idx:
            sid = subjects[i]
            conn = load_subject_connectivity(sid)

            for ep in conn:
                Xtr.append(ep.flatten() if model_name == "ANN" else ep)
                ytr.append(labels[sid])

        # ---- Testing data (epoch-wise)
        for i in test_idx:
            sid = subjects[i]
            conn = load_subject_connectivity(sid)

            for ep in conn:
                Xte.append(ep.flatten() if model_name == "ANN" else ep)
                yte.append(labels[sid])
                sid_te.append(sid)

        Xtr = torch.tensor(Xtr, dtype=torch.float32)
        ytr = torch.tensor(ytr, dtype=torch.long)
        Xte = torch.tensor(Xte, dtype=torch.float32)

        model = model_class().to(DEVICE)
        optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        criterion = nn.CrossEntropyLoss()

        # ---- Train (light training by design)
        model.train()
        for _ in range(EPOCHS):
            optimizer.zero_grad()
            outputs = model(Xtr)
            loss = criterion(outputs, ytr)
            loss.backward()
            optimizer.step()

        # ---- Evaluate (subject-wise aggregation)
        model.eval()
        with torch.no_grad():
            probs = torch.softmax(model(Xte), dim=1)[:, 1].numpy()

        subj_probs = {}
        for p, sid in zip(probs, sid_te):
            subj_probs.setdefault(sid, []).append(p)

        y_true, y_pred, y_score = [], [], []

        for sid, ps in subj_probs.items():
            mean_prob = np.mean(ps)
            y_score.append(mean_prob)
            y_pred.append(int(mean_prob >= 0.5))
            y_true.append(labels[sid])

        fold_results.append([
            accuracy_score(y_true, y_pred),
            precision_score(y_true, y_pred, zero_division=0),
            recall_score(y_true, y_pred, zero_division=0),
            f1_score(y_true, y_pred, zero_division=0),
            roc_auc_score(y_true, y_score)
        ])

    return np.mean(fold_results, axis=0)


# =====================
# Run all baselines
# =====================
results = []

for name, model in [
    ("ANN", ANN),
    ("RNN", RNNModel),
    ("BiLSTM", BiLSTM)
]:
    print(f"\nRunning {name}...")
    acc, prec, rec, f1, auc = run_model(model, name)
    results.append([name, acc, prec, rec, f1, auc])


# =====================
# Save results
# =====================
df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
)

df.to_csv(RESULT_DIR / "baseline_comparison.csv", index=False)

print("\nSaved to result/baselines/baseline_comparison.csv")
print(df)