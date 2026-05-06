import numpy as np
import matplotlib.pyplot as plt

conn = np.load("data/processed/connectivity/sub-056_conn.npy")

plt.figure(figsize=(5, 4))
plt.imshow(conn[0], cmap="jet")
plt.colorbar(label="Correlation")
plt.title("Connectivity matrix (Epoch 1)")
plt.tight_layout()
plt.show()