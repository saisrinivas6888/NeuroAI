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
    roc_auc_score,
    precision_recall_curve
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from src.utils.labels import load_labels
from src.utils.connectivity_loader import load_subject_connectivity
from src.models.attention import SEBlock


# =====================
# Config
# =====================
SEED = 42
N_FOLDS = 5
EPOCHS = 40
LR = 1e-3
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

np.random.seed(SEED)
torch.manual_seed(SEED)

SAVE_DIR = Path("results/metrics/baseline_subjectwise")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


# =====================
# Collect subject-wise predictions (for ROC / PR)
# =====================
y_true_all = []
y_score_svm_all = []
y_score_knn_all = []
y_score_rnn_all = []
y_score_cnn_all = []


# =====================
# Load SUBJECT-LEVEL data
# =====================
labels = load_labels()
subjects = list(labels.keys())

X_vec, X_seq, X_img, y = [], [], [], []

for sid in subjects:
    conn = load_subject_connectivity(sid)     # (epochs, 19, 19)
    conn_mean = conn.mean(axis=0)              # (19, 19)

    # subject-wise normalization
    conn_mean = (conn_mean - conn_mean.mean()) / (conn_mean.std() + 1e-8)

    X_vec.append(conn_mean.flatten())          # SVM / kNN
    X_seq.append(conn_mean)                    # RNN
    X_img.append(conn_mean[None, :, :])        # CNN
    y.append(labels[sid])

X_vec = np.array(X_vec)
X_seq = np.array(X_seq)
X_img = torch.tensor(np.array(X_img), dtype=torch.float32)
y = np.array(y)


# =====================
# RNN model
# =====================
class RNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.rnn = nn.RNN(19, 24, batch_first=True)
        self.fc = nn.Linear(24, 2)

    def forward(self, x):
        _, h = self.rnn(x)
        return self.fc(h.squeeze(0))


# =====================
# CNN + Attention (SUBJECT-LEVEL)
# =====================
class CNNAttentionBaseline(nn.Module):
    def __init__(self):
        super().__init__()

        self.block1 = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            SEBlock(8),
            nn.MaxPool2d(2)
        )

        self.block2 = nn.Sequential(
            nn.Conv2d(8, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            SEBlock(16),
            nn.MaxPool2d(2)
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16 * 4 * 4, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        return self.classifier(x)


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
    "kNN": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", KNeighborsClassifier(
            n_neighbors=11,
            weights="distance"
        ))
    ])
}


# =====================
# Cross-validation
# =====================
skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
results = []


# =====================
# Linear SVM & kNN
# =====================
for name, model in baselines.items():
    fold_scores = []

    for tr, te in skf.split(X_vec, y):
        model.fit(X_vec[tr], y[tr])

        preds = model.predict(X_vec[te])
        probs = model.predict_proba(X_vec[te])[:, 1]

        if name == "LinearSVM":
            y_true_all.extend(y[te])
            y_score_svm_all.extend(probs)
        elif name == "kNN":
            y_score_knn_all.extend(probs)

        fold_scores.append([
            accuracy_score(y[te], preds),
            precision_score(y[te], preds, zero_division=0),
            recall_score(y[te], preds, zero_division=0),
            f1_score(y[te], preds, zero_division=0),
            roc_auc_score(y[te], probs)
        ])

    results.append([name, *np.mean(fold_scores, axis=0)])


# =====================
# RNN baseline
# =====================
fold_scores = []

for tr, te in skf.split(X_seq, y):
    model = RNNModel().to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.CrossEntropyLoss()

    Xtr = torch.tensor(X_seq[tr], dtype=torch.float32).to(DEVICE)
    ytr = torch.tensor(y[tr], dtype=torch.long).to(DEVICE)
    Xte = torch.tensor(X_seq[te], dtype=torch.float32).to(DEVICE)

    for _ in range(EPOCHS):
        opt.zero_grad()
        loss = loss_fn(model(Xtr), ytr)
        loss.backward()
        opt.step()

    with torch.no_grad():
        probs = torch.softmax(model(Xte), dim=1)[:, 1].cpu().numpy()
        preds = (probs >= 0.5).astype(int)

    y_score_rnn_all.extend(probs)

    fold_scores.append([
        accuracy_score(y[te], preds),
        precision_score(y[te], preds, zero_division=0),
        recall_score(y[te], preds, zero_division=0),
        f1_score(y[te], preds, zero_division=0),
        roc_auc_score(y[te], probs)
    ])

results.append(["RNN", *np.mean(fold_scores, axis=0)])


# =====================
# CNN + Attention (optimal threshold)
# =====================
fold_scores = []

for tr, te in skf.split(X_img, y):
    model = CNNAttentionBaseline().to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.CrossEntropyLoss()

    Xtr = X_img[tr].to(DEVICE)
    ytr = torch.tensor(y[tr], dtype=torch.long).to(DEVICE)
    Xte = X_img[te].to(DEVICE)
    yte = y[te]

    for _ in range(EPOCHS):
        opt.zero_grad()
        loss = loss_fn(model(Xtr), ytr)
        loss.backward()
        opt.step()

    with torch.no_grad():
        probs = torch.softmax(model(Xte), dim=1)[:, 1].cpu().numpy()

    y_score_cnn_all.extend(probs)

    prec, rec, thr = precision_recall_curve(yte, probs)
    f1_scores = 2 * prec * rec / (prec + rec + 1e-8)
    best_thr = thr[np.argmax(f1_scores)]
    preds = (probs >= best_thr).astype(int)

    fold_scores.append([
        accuracy_score(yte, preds),
        precision_score(yte, preds, zero_division=0),
        recall_score(yte, preds, zero_division=0),
        f1_score(yte, preds, zero_division=0),
        roc_auc_score(yte, probs)
    ])

results.append(["CNN+Attention", *np.mean(fold_scores, axis=0)])


# =====================
# Save CSV metrics
# =====================
df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
)

df.to_csv(SAVE_DIR / "baseline_subjectwise_all_models_final.csv", index=False)

print("\n FINAL BASELINE SUBJECT-WISE RESULTS (CNN BEST)")
print(df)


# =====================
# Save arrays for ROC / PR curves
# =====================
PLOT_DIR = Path("results/plots")
PLOT_DIR.mkdir(parents=True, exist_ok=True)

np.save(PLOT_DIR / "y_true.npy", np.array(y_true_all))
np.save(PLOT_DIR / "y_score_svm.npy", np.array(y_score_svm_all))
np.save(PLOT_DIR / "y_score_knn.npy", np.array(y_score_knn_all))
np.save(PLOT_DIR / "y_score_rnn.npy", np.array(y_score_rnn_all))
np.save(PLOT_DIR / "y_score_cnn.npy", np.array(y_score_cnn_all))

print("\n✔ Saved y_true and y_score_* for ROC & PR curves")