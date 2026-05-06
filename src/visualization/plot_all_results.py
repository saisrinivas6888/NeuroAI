import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import (
    roc_curve, auc,
    precision_recall_curve,
    average_precision_score
)

# =====================
# Paths
# =====================
PLOT_DIR = Path("results/plots")
PLOT_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = Path("results/metrics/baseline_subjectwise/baseline_subjectwise_all_models_final.csv")

# =====================
# Load arrays (for ROC / PR)
# =====================
y_true = np.load(PLOT_DIR / "y_true.npy")
y_score_svm = np.load(PLOT_DIR / "y_score_svm.npy")
y_score_knn = np.load(PLOT_DIR / "y_score_knn.npy")
y_score_rnn = np.load(PLOT_DIR / "y_score_rnn.npy")
y_score_cnn = np.load(PLOT_DIR / "y_score_cnn.npy")

models_scores = {
    "Linear SVM": y_score_svm,
    "kNN": y_score_knn,
    "RNN": y_score_rnn,
    "CNN + Attention": y_score_cnn
}

# =====================
# 1️⃣ ROC CURVE
# =====================
plt.figure(figsize=(8.5, 7.5))

for name, scores in models_scores.items():
    fpr, tpr, _ = roc_curve(y_true, scores)
    roc_auc = auc(fpr, tpr)

    plt.plot(
        fpr, tpr,
        linewidth=3 if "CNN" in name else 2,
        label=f"{name} (AUC = {roc_auc:.3f})"
    )

plt.plot([0, 1], [0, 1], "--", color="gray", linewidth=2, alpha=0.6)

plt.xlabel("False Positive Rate", fontsize=14)
plt.ylabel("True Positive Rate", fontsize=14)
plt.title("ROC Curves ", fontsize=16, pad=15)
plt.legend(loc="lower right", fontsize=12, frameon=True)
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(PLOT_DIR / "roc_curve_subjectwise.png", dpi=600)
plt.close()

# =====================
# 2️⃣ PRECISION–RECALL CURVE
# =====================
plt.figure(figsize=(8.5, 7.5))

for name, scores in models_scores.items():
    precision, recall, _ = precision_recall_curve(y_true, scores)
    ap = average_precision_score(y_true, scores)

    plt.plot(
        recall, precision,
        linewidth=3 if "CNN" in name else 2,
        label=f"{name} (AP = {ap:.3f})"
    )

plt.xlabel("Recall", fontsize=14)
plt.ylabel("Precision", fontsize=14)
plt.title("Precision–Recall Curves", fontsize=17, pad=16)
plt.legend(loc="lower left", fontsize=13, frameon=True)
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(PLOT_DIR / "pr_curve_subjectwise.png", dpi=600)
plt.close()

# =====================
# Load CSV metrics
# =====================
df = pd.read_csv(CSV_PATH)

order = ["LinearSVM", "kNN", "RNN", "CNN+Attention"]
df["Model"] = pd.Categorical(df["Model"], categories=order, ordered=True)
df = df.sort_values("Model")

# =====================
# 3️⃣ Accuracy & F1 bar chart
# =====================
plt.figure(figsize=(9, 6))

x = np.arange(len(df))
width = 0.35

plt.bar(x - width/2, df["Accuracy"], width, label="Accuracy")
plt.bar(x + width/2, df["F1"], width, label="F1-score")

plt.xticks(x, df["Model"], fontsize=13)
plt.ylabel("Score", fontsize=13)
plt.title("Accuracy and F1-score Comparison ", fontsize=18)
plt.ylim(0.6, 0.9)

plt.legend(frameon=True)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(PLOT_DIR / "accuracy_f1_comparison.png", dpi=600)
plt.close()

# =====================
# 4️⃣ ROC-AUC bar chart
# =====================
plt.figure(figsize=(9, 6))

plt.bar(df["Model"], df["ROC-AUC"], color=["gray", "steelblue", "orange", "crimson"])

plt.ylabel("ROC-AUC", fontsize=13)
plt.title("ROC-AUC Comparison ", fontsize=18)
plt.ylim(0.6, 0.9)

for i, v in enumerate(df["ROC-AUC"]):
    plt.text(i, v + 0.01, f"{v:.3f}", ha="center", fontsize=13)

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(PLOT_DIR / "roc_auc_comparison.png", dpi=600)
plt.close()

print("✔ All visualizations saved in results/plots/")

