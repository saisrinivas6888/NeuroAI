import sys
from pathlib import Path
import torch
import numpy as np

# add project root to python path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from src.models.cnn_attention import CNNAttention

DEVICE = "cpu"

model = CNNAttention()
model.load_state_dict(torch.load(ROOT / "cnn_attention_subjectwise.pth", map_location=DEVICE))
model.eval()


def predict(connectivity_matrix):

    x = torch.tensor(connectivity_matrix, dtype=torch.float32)
    x = x.unsqueeze(0).unsqueeze(0)

    with torch.no_grad():
        output = model(x)
        prob = torch.softmax(output, dim=1)[0, 1].item()

    prediction = "Alzheimer" if prob >= 0.5 else "Control"

    return prediction, prob