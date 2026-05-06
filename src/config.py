# src/config.py
from pathlib import Path

# ========================
# Paths
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

EPOCHS_DIR = PROCESSED_DATA_DIR / "epochs"
CONNECTIVITY_DIR = PROCESSED_DATA_DIR / "connectivity"

EPOCHS_DIR.mkdir(parents=True, exist_ok=True)
CONNECTIVITY_DIR.mkdir(parents=True, exist_ok=True)

# ========================
# EEG preprocessing params
# ========================
LOW_FREQ = 0.5
HIGH_FREQ = 45.0
EPOCH_LENGTH = 2.0      # seconds
OVERLAP = 0.5           # 50%

# ========================
# Labels (A vs C)
# ========================
LABEL_MAP = {
    "C": 0,   # Healthy Control
    "A": 1    # Alzheimer Disease
}

print("DEBUG config.py loaded")