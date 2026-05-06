import torch
import numpy as np
import pandas as pd
from pathlib import Path

from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from src.training.dataset import ConnectivityDataset
from src.models.cnn_attention import CNNAttention


# =====================
# Create output directory
# =====================
Path("results/metrics/cnn_attention").mkdir(parents=True, exist_ok=True)


# =====================
# Dataset
# =====================
dataset = ConnectivityDataset()

indices = list(range(len(dataset)))
train_idx, test_idx = train_test_split(
    indices, test_size=0.2, random_state=42, shuffle=True
)

train_loader = DataLoader(
    torch.utils.data.Subset(dataset, train_idx),
    batch_size=32,
    shuffle=True
)

test_loader = DataLoader(
    torch.utils.data.Subset(dataset, test_idx),
    batch_size=32,
    shuffle=False
)


# =====================
# Model
# =====================
model = CNNAttention()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

EPOCHS = 10


# =====================
# Epoch-level evaluation
# =====================
def evaluate_epoch_level(model, loader):
    model.eval()

    y_true, y_pred, y_score = [], [], []

    with torch.no_grad():
        for x, y in loader:
            logits = model(x)
            probs = torch.softmax(logits, dim=1)[:, 1]

            y_true.extend(y.cpu().numpy())
            y_score.extend(probs.cpu().numpy())
            y_pred.extend((probs >= 0.5).cpu().numpy())

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    auc = roc_auc_score(y_true, y_score)

    # =====================
    # SAVE epoch-level results (CSV)
    # =====================
    df_epoch = pd.DataFrame({
        "y_true": y_true,
        "y_score": y_score,
        "y_pred": y_pred
    })

    df_epoch.to_csv(
        "results/metrics/cnn_attention/cnn_attention_epoch_level.csv",
        index=False
    )

    return acc, prec, rec, f1, auc


# =====================
# Training
# =====================
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0.0

    for x, y in train_loader:
        optimizer.zero_grad()
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    acc, prec, rec, f1, auc = evaluate_epoch_level(model, test_loader)

    print(
        f"Epoch {epoch+1}/{EPOCHS} | "
        f"Loss: {total_loss:.4f} | "
        f"Acc: {acc:.3f} | "
        f"Prec: {prec:.3f} | "
        f"Recall: {rec:.3f} | "
        f"F1: {f1:.3f} | "
        f"AUC: {auc:.3f}"
    )


# =====================
# Final Evaluation
# =====================
model.eval()
correct, total = 0, 0

with torch.no_grad():
    for x, y in test_loader:
        preds = model(x).argmax(dim=1)
        correct += (preds == y).sum().item()
        total += y.size(0)

print(f"\nFinal Test Accuracy (Epoch-level): {correct / total:.3f}")