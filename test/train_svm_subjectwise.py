import numpy as np
from pathlib import Path

from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.utils.labels import load_labels

# =====================
# Paths
# =====================
DATA_DIR = Path("data/processed/connectivity")
SAVE_DIR = Path("result/metrics/svm_subjectwise")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# =====================
# Load labels (subject-wise)
# =====================
labels = load_labels()
subjects = list(labels.keys())
y = np.array([labels[s] for s in subjects])

# =====================
# Load subject-wise features
# =====================
X = []

# Upper triangle indices (avoid redundancy)
tri_idx = np.triu_indices(19, k=1)

for s in subjects:
    conn = np.load(DATA_DIR / f"{s}_conn.npy")  # (epochs, 19, 19)
    conn = conn[:, tri_idx[0], tri_idx[1]]      # (epochs, ~171)
    subj_feat = conn.mean(axis=0)               # (171,)
    X.append(subj_feat)

X = np.array(X)

# =====================
# Subject-wise CV
# =====================
skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

results = []

for fold, (train_idx, test_idx) in enumerate(skf.split(X, y), 1):

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(
            kernel="rbf",
            probability=True,
            class_weight="balanced",
            random_state=42
        ))
    ])

    model.fit(X[train_idx], y[train_idx])

    y_pred = model.predict(X[test_idx])
    y_score = model.predict_proba(X[test_idx])[:, 1]

    acc = accuracy_score(y[test_idx], y_pred)
    f1 = f1_score(y[test_idx], y_pred)
    auc = roc_auc_score(y[test_idx], y_score)

    print(f"Fold {fold} → Acc: {acc:.3f}, F1: {f1:.3f}, AUC: {auc:.3f}")
    results.append((acc, f1, auc))

# =====================
# Save results
# =====================
results = np.array(results)
np.save(SAVE_DIR / "fold_results.npy", results)

print("\n📊 SVM SUBJECT-WISE RESULTS")
print(f"Accuracy : {results[:, 0].mean():.3f}")
print(f"F1-score : {results[:, 1].mean():.3f}")
print(f"ROC-AUC  : {results[:, 2].mean():.3f}")