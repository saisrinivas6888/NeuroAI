# src/training/train_subjectwise.py
import torch
import numpy as np
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.utils.labels import load_labels
from src.training.dataset_subjectwise import SubjectWiseConnectivityDataset
from src.models.cnn_attention import CNNAttention   # change to CNNBaseline for baseline


# =====================
# Subject-wise split
# =====================
labels = load_labels()
subjects = list(labels.keys())

train_subjects, test_subjects = train_test_split(
    subjects, test_size=0.2, random_state=42, shuffle=True
)

print(f"Train subjects: {len(train_subjects)}")
print(f"Test subjects: {len(test_subjects)}")

train_ds = SubjectWiseConnectivityDataset(train_subjects)
test_ds = SubjectWiseConnectivityDataset(test_subjects)

train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
test_loader = DataLoader(test_ds, batch_size=32, shuffle=False)

# =====================
# Model
# =====================
model = CNNAttention()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# =====================
# Training
# =====================
for epoch in range(10):
    model.train()
    total_loss = 0.0

    for x, y, _ in train_loader:
        optimizer.zero_grad()
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

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

# Aggregate epoch predictions → subject prediction
y_true, y_pred, y_score = [], [], []

for s in subject_probs:
    mean_prob = np.mean(subject_probs[s])
    y_score.append(mean_prob)
    y_pred.append(1 if mean_prob >= 0.5 else 0)
    y_true.append(subject_labels[s])

# Metrics
acc = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
auc = roc_auc_score(y_true, y_score)

print("SUBJECT-WISE RESULTS ")
print(f"Accuracy : {acc:.3f}")
print(f"F1-score : {f1:.3f}")
print(f"ROC-AUC  : {auc:.3f}")

# Save trained model
torch.save(model.state_dict(), "cnn_attention_subjectwise.pth")
print("\n Model saved as cnn_attention_subjectwise.pth")