import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score
from scipy.interpolate import make_interp_spline
from pathlib import Path

# =====================
# BASE PATH (robust)
# =====================
BASE_DIR = Path(__file__).resolve().parents[2]

# =====================
# DATA PATH (correct)
# =====================
DATA_DIR = BASE_DIR / "results" / "plots"

# =====================
# LOAD DATA
# =====================
y_true = np.load(DATA_DIR / "y_true.npy")
y_score = np.load(DATA_DIR / "y_score_cnn.npy")   # ✅ correct file

# =====================
# STYLE
# =====================
plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# =====================
# COMPUTE PR
# =====================
precision, recall, _ = precision_recall_curve(y_true, y_score)
ap = average_precision_score(y_true, y_score)

# =====================
# BASELINE
# =====================
baseline = np.mean(y_true)

# =====================
# SMOOTH FUNCTION
# =====================
def smooth_curve(x, y):
    x, y = zip(*sorted(zip(x, y)))
    x = np.array(x)
    y = np.array(y)

    unique_idx = np.unique(x, return_index=True)[1]
    x = x[unique_idx]
    y = y[unique_idx]

    if len(x) < 4:
        return x, y

    x_new = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)
    y_smooth = spline(x_new)

    return x_new, y_smooth

# =====================
# SMOOTH CURVE
# =====================
recall_s, precision_s = smooth_curve(recall, precision)

# =====================
# PLOT
# =====================
plt.figure(figsize=(5.5,4.5))

plt.plot(
    recall_s,
    precision_s,
    lw=2.5,
    color="#1f77b4",
    label=f"Proposed Model (AP = {ap:.3f})"
)

plt.hlines(
    baseline,
    0, 1,
    colors="gray",
    linestyles="dashed",
    linewidth=1.5,
    label="No-skill baseline"
)

plt.fill_between(recall_s, precision_s, alpha=0.08)

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision–Recall Curve for AD Detection (Subject-wise)")

plt.xlim(0, 1)
plt.ylim(0, 1)

plt.legend(loc="lower left", frameon=False)
plt.grid(alpha=0.25)

plt.tight_layout()

# =====================
# SAVE (correct)
# =====================
SAVE_PATH = DATA_DIR / "pr_curve_subjectwise_clean.png"

plt.savefig(SAVE_PATH, dpi=600, bbox_inches="tight")

plt.show()