# src/utils/labels.py

import pandas as pd
from src.config import RAW_DATA_DIR, LABEL_MAP


def load_labels():
    tsv_path = RAW_DATA_DIR / "participants.tsv"
    df = pd.read_csv(tsv_path, sep="\t")

    print("DEBUG LABEL_MAP inside labels.py:", LABEL_MAP)
    print("DEBUG Unique Group values:", df["Group"].unique())

    labels = {}
    skipped = 0

    for _, row in df.iterrows():
        subject_id = row["participant_id"]
        group = str(row["Group"]).strip().upper()

        if group not in LABEL_MAP:
            skipped += 1
            continue

        labels[subject_id] = LABEL_MAP[group]

    print(f"✔ Labels loaded: {len(labels)} subjects")
    print(f"⚠ Skipped subjects: {skipped}")
    return labels