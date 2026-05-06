import torch
import numpy as np
import pandas as pd
from pathlib import Path
from torch.utils.data import DataLoader
from sklearn.model_selection import KFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from src.utils.labels import load_labels
from src.training.dataset_subjectwise import SubjectWiseConnectivityDataset
from src.models.cnn_attention import CNNAttention


# =====================
# Setup
# =====================
NUM_FOLDS = 5
BATCH_SIZE = 32
EPOCHS = 10
LR = 1e-3
SEED = 42

torch.manual_seed(SEED)
np.random.seed(SEED)

SAVE_DIR = Path("results/metrics/subjectwise_cv")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

labels = load_labels()
subjects = np.array(list(labels.keys()))

kf = KFold(n_splits=NUM_FOLDS, shuffle=True, random_state=SEED)

# Global storage (across folds)
all_y_true = []
all_y_pred = []
all_y_score = []
all_subjects = []
fold_log = []

# =====================
# Cross-validation
# =====================
for fold, (train_idx, test_idx) in enumerate(kf.split(subjects), 1):
    print("\n==============================")
    print(f"Fold {fold}/{NUM_FOLDS}")
    print("==============================")

    train_subjects = subjects[train_idx].tolist()
    test_subjects = subjects[test_idx].tolist()

    print(f"Train subjects: {len(train_subjects)}")
    print(f"Test subjects : {len(test_subjects)}")

    train_ds = SubjectWiseConnectivityDataset(train_subjects)
    test_ds = SubjectWiseConnectivityDataset(test_subjects)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False)

    model = CNNAttention()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    # =====================
    # Training
    # =====================
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0

        for x, y, _ in train_loader:
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss:.4f}")

    # =====================
    # Subject-wise Evaluation
    # =====================
    model.eval()
    subject_probs = {}
    subject_labels = {}

    with torch.no_grad():
        for x, y, sid in test_loader:
            probs = torch.softmax(model(x), dim=1)[:, 1].cpu().numpy()

            for i in range(len(sid)):
                s = sid[i]
                if s not in subject_probs:
                    subject_probs[s] = []
                    subject_labels[s] = y[i].item()
                subject_probs[s].append(probs[i])

    # Aggregate epochs → subject
    y_true, y_pred, y_score = [], [], []

    for s in subject_probs:
        mean_prob = np.mean(subject_probs[s])
        y_score.append(mean_prob)
        y_pred.append(1 if mean_prob >= 0.5 else 0)
        y_true.append(subject_labels[s])

    # Metrics
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_score)

    print(
        f"Fold {fold} results → "
        f"Acc: {acc:.3f}, "
        f"Prec: {prec:.3f}, "
        f"Recall: {rec:.3f}, "
        f"F1: {f1:.3f}, "
        f"AUC: {auc:.3f}"
    )

    # Save fold results
    fold_log.append({
        "fold": fold,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "auc": auc
    })

    # Accumulate subject-wise predictions
    all_y_true.extend(y_true)
    all_y_pred.extend(y_pred)
    all_y_score.extend(y_score)
    all_subjects.extend(list(subject_probs.keys()))

# =====================
# Save metrics
# =====================
np.save(SAVE_DIR / "y_true.npy", np.array(all_y_true))
np.save(SAVE_DIR / "y_pred.npy", np.array(all_y_pred))
np.save(SAVE_DIR / "y_score.npy", np.array(all_y_score))
np.save(SAVE_DIR / "subjects.npy", np.array(all_subjects))

pd.DataFrame(fold_log).to_csv(SAVE_DIR / "fold_metrics.csv", index=False)

# =====================
# Final Results
# =====================
fold_results = pd.DataFrame(fold_log)

print("\n==============================")
print("📊 5-FOLD SUBJECT-WISE RESULTS")
print("==============================")
print(f"Accuracy  : {fold_results.accuracy.mean():.3f} ± {fold_results.accuracy.std():.3f}")
print(f"Precision : {fold_results.precision.mean():.3f} ± {fold_results.precision.std():.3f}")
print(f"Recall    : {fold_results.recall.mean():.3f} ± {fold_results.recall.std():.3f}")
print(f"F1-score  : {fold_results.f1.mean():.3f} ± {fold_results.f1.std():.3f}")
print(f"ROC-AUC   : {fold_results.auc.mean():.3f} ± {fold_results.auc.std():.3f}")

print(f"\n✔ Metrics saved to: {SAVE_DIR}")