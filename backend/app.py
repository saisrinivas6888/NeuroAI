from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import os
import mne
import time
from model_loader import predict

# importing existing pipeline modules
from src.data.preprocess import preprocess_raw
from src.data.epoching import make_epochs
from src.features.connectivity import save_subject_connectivity

app = FastAPI()

# Allowing frontend (Next.js) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# temp storage folder
TMP_DIR = "tmp"
os.makedirs(TMP_DIR, exist_ok=True)


# =========================
# Root route
# =========================
@app.get("/")
def home():
    return {"message": "EEG Alzheimer Detection API running"}


# =========================
# Prediction route
# =========================
@app.post("/predict")
async def predict_eeg(data: dict):

    try:
        file_path = data.get("filePath")

        if not file_path:
            return {"error": "No filePath provided"}

        print(" Loading file:", file_path)

        #  check file exists
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        #  Load matrix
        matrix = np.load(file_path, allow_pickle=True)

        print(" Raw shape:", getattr(matrix, "shape", None))
        print(" dtype:", getattr(matrix, "dtype", None))

        # ensure numpy array
        matrix = np.array(matrix)

        #  Handle epoch-level
        if matrix.ndim == 3:
            print("⚙️ Averaging epochs...")
            matrix = matrix.mean(axis=0)

        print(" Final shape:", matrix.shape)

        # validate
        if matrix.shape != (19, 19):
            return {
                "error": f"Invalid matrix shape {matrix.shape}. Expected (19,19)"
            }

        # clean
        matrix = np.nan_to_num(matrix)

        #  prediction
        prediction, prob = predict(matrix)

        print(" Prediction:", prediction)
        print(" Confidence:", prob)

        return {
            "prediction": prediction,
            "confidence": float(prob)
        }

    except Exception as e:
        print(" ERROR:", str(e))
        return {"error": str(e)}


# =========================
# EEG PREPROCESSING ROUTE
# =========================
@app.post("/preprocess")
async def preprocess_eeg(file: UploadFile):

    try:
        # Save uploaded EEG file
        filepath = os.path.join(TMP_DIR, file.filename)

        with open(filepath, "wb") as f:
            f.write(await file.read())

        print(f" Uploaded EEG saved to: {filepath}")

        # Load EEG
        raw = mne.io.read_raw_eeglab(filepath, preload=True)

        # Preprocess
        raw = preprocess_raw(raw)

        # Epochs
        epochs = make_epochs(raw)

        epochs_path = os.path.join(TMP_DIR, "epochs-epo.fif")
        epochs.save(epochs_path, overwrite=True)

        print(" Epochs generated")

        # Connectivity
        subject_id = "web_user"
        conn = save_subject_connectivity(subject_id, epochs)

        if conn is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            possible_path = os.path.join(
                base_dir,
                "data",
                "processed",
                "connectivity",
                f"{subject_id}_conn.npy"
            )
            print(" Looking for connectivity file at:", possible_path)
            if os.path.exists(possible_path):
                conn = np.load(possible_path)
                print(" Connectivity loaded from disk")
            else:
                raise Exception(f" File not found: {possible_path}")

        #  CRITICAL FIX no pickle issues
        conn = np.array(conn, dtype=np.float32)
        conn = np.nan_to_num(conn)

        print(" Connectivity shape:", conn.shape)
        print(" dtype:", conn.dtype)

        # Save matrix
        conn_path = os.path.join(TMP_DIR, f"matrix_{int(time.time())}.npy")
        np.save(conn_path, conn)

        print(" Connectivity matrix saved:", conn_path)

        return {
            "success": True,
            "file_path": conn_path
        }

    except Exception as e:
        print(" ERROR:", str(e))
        return {"error": str(e)}