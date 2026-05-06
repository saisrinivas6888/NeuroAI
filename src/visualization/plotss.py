import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import (
    roc_curve, auc,
    precision_recall_curve,
    average_precision_score
)
from scipy.interpolate import make_interp_spline

# =====================
# STYLE (clean + controlled)
# =====================
plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "legend.fontsize": 11,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.linewidth": 1.2
})

# =====================
# Paths
# =====================
PLOT_DIR = Path("results/plots")
PLOT_DIR.mkdir(parents=True, exist_ok=True)

# =====================
# Load Data
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
# FUNCTION: SMOOTH CURVE
# =====================
def smooth_curve(x, y):
    x, y = zip(*sorted(zip(x, y)))  # ensure sorted
    x = np.array(x)
    y = np.array(y)

    # remove duplicates (important!)
    unique_idx = np.unique(x, return_index=True)[1]
    x = x[unique_idx]
    y = y[unique_idx]

    if len(x) < 4:
        return x, y  # not enough points to smooth

    x_new = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)
    y_smooth = spline(x_new)

    return x_new, y_smooth

# =====================
# 1️⃣ ROC CURVE (SMOOTH)
# =====================
plt.figure(figsize=(6,5))

for name, scores in models_scores.items():
    fpr, tpr, _ = roc_curve(y_true, scores)
    roc_auc = auc(fpr, tpr)

    fpr_s, tpr_s = smooth_curve(fpr, tpr)

    plt.plot(
        fpr_s, tpr_s,
        linewidth=2.5 if "CNN" in name else 2,
        label=f"{name} (AUC = {roc_auc:.3f})"
    )

# diagonal line
plt.plot([0, 1], [0, 1], '--', color='gray', linewidth=1)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves")
plt.legend(loc="lower right", frameon=False)
plt.grid(alpha=0.2)

plt.tight_layout()
plt.savefig(PLOT_DIR / "roc_curve_upsubjectwise.png", dpi=600, bbox_inches="tight")
plt.close()

# =====================
# 2️⃣ PR CURVE (SMOOTH)
# =====================
plt.figure(figsize=(6,5))

for name, scores in models_scores.items():
    precision, recall, _ = precision_recall_curve(y_true, scores)
    ap = average_precision_score(y_true, scores)

    recall_s, precision_s = smooth_curve(recall, precision)

    plt.plot(
        recall_s, precision_s,
        linewidth=2.5 if "CNN" in name else 2,
        label=f"{name} (AP = {ap:.3f})"
    )

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision–Recall Curves")
plt.legend(loc="lower left", frameon=False)
plt.grid(alpha=0.2)

plt.tight_layout()
plt.savefig(PLOT_DIR / "pr_curve_upsubjectwise.png", dpi=600, bbox_inches="tight")
plt.close()