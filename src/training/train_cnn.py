# src/training/train_cnn.py
import torch
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from src.training.dataset import ConnectivityDataset
from src.models.cnn_baseline import CNNBaseline

# Dataset
dataset = ConnectivityDataset()
indices = list(range(len(dataset)))
train_idx, test_idx = train_test_split(
    indices, test_size=0.2, random_state=42, shuffle=True
)

train_loader = DataLoader(
    torch.utils.data.Subset(dataset, train_idx),
    batch_size=32, shuffle=True
)
test_loader = DataLoader(
    torch.utils.data.Subset(dataset, test_idx),
    batch_size=32, shuffle=False
)

# Model
model = CNNBaseline()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# Training
for epoch in range(10):
    model.train()
    total_loss = 0

    for x, y in train_loader:
        optimizer.zero_grad()
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

# Evaluation
model.eval()
correct, total = 0, 0
with torch.no_grad():
    for x, y in test_loader:
        preds = model(x).argmax(dim=1)
        correct += (preds == y).sum().item()
        total += y.size(0)

print(f"Test Accuracy: {correct / total:.3f}")