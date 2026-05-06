import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

from src.utils.labels import load_labels
from src.utils.connectivity_loader import load_subject_connectivity


# =====================
# Config
# =====================
N_FOLDS = 5
SEED = 42

SAVE_DIR = Path("results/metrics/safe_baselines")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


# =====================
# Load subject-level data
# =====================
labels = load_labels()
subjects = list(labels.keys())

X, y = [], []

for sid in subjects:
    conn = load_subject_connectivity(sid)   # (epochs, 19, 19)
    conn_mean = conn.mean(axis=0)            # (19, 19)
    X.append(conn_mean.flatten())            # (361,)
    y.append(labels[sid])

X = np.array(X)
y = np.array(y)


# =====================
# Models (INTENTIONALLY SIMPLE)
# =====================
models = {
    "LogisticRegression": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=SEED
        ))
    ]),

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
        ("clf", KNeighborsClassifier(n_neighbors=5))
    ]),

    "NaiveBayes": GaussianNB(),

    "DecisionTree": DecisionTreeClassifier(
        max_depth=4,
        random_state=SEED,
        class_weight="balanced"
    )
}


# =====================
# 5-Fold Subject-wise CV
# =====================
skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=SEED
)

results = []

for name, model in models.items():
    print(f"\nRunning {name}...")
    fold_metrics = []

    for train_idx, test_idx in skf.split(X, y):

        model.fit(X[train_idx], y[train_idx])

        y_pred = model.predict(X[test_idx])

        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X[test_idx])[:, 1]
        else:
            y_score = model.decision_function(X[test_idx])

        fold_metrics.append([
            accuracy_score(y[test_idx], y_pred),
            precision_score(y[test_idx], y_pred, zero_division=0),
            recall_score(y[test_idx], y_pred, zero_division=0),
            f1_score(y[test_idx], y_pred, zero_division=0),
            roc_auc_score(y[test_idx], y_score)
        ])

    mean = np.mean(fold_metrics, axis=0)
    results.append([name, *mean])


# =====================
# Save results
# =====================
df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
)

df.to_csv(SAVE_DIR / "safe_baseline_comparison.csv", index=False)

print("\n📊 SAFE BASELINE RESULTS (SUBJECT-WISE)")
print(df)
print(f"\nSaved to {SAVE_DIR / 'safe_baseline_comparison.csv'}")