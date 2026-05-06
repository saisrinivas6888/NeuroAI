from src.training.dataset import ConnectivityDataset

dataset = ConnectivityDataset()

print("len(dataset):", len(dataset))
print("len(dataset.subjects):", len(dataset.subjects))
print("First 10 dataset.subjects:", dataset.subjects[:10])