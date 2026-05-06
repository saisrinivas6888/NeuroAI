# NeuroAI

AI-powered EEG Analysis and Alzheimer Detection Platform using CNN + Attention Architecture.

---

# Overview

NeuroAI is an advanced EEG-based deep learning platform designed for neurological analysis and early Alzheimer’s disease prediction.

The system combines:

* EEG preprocessing
* Connectivity matrix generation
* CNN + Attention deep learning
* Patient management
* Prediction tracking
* Interactive clinical dashboard

The platform is designed with a modern full-stack architecture integrating AI workflows with an interactive medical-style UI.

---

# Features

## AI Prediction System

* CNN + Attention hybrid architecture
* EEG connectivity matrix classification
* Confidence score generation
* Fast inference pipeline

## EEG Preprocessing

* Upload EEG `.set` files
* Automated preprocessing pipeline
* Connectivity matrix generation
* Matrix storage for AI inference

## Patient Management

* Add patients
* Edit patient details
* Delete patients
* View patient records
* Search patients instantly

## History Tracking

* Prediction history dashboard
* Confidence visualization
* Historical patient analysis tracking
* Searchable analysis records

## User Interface

* Modern glassmorphism design
* Animated dashboard
* Responsive layouts
* Smooth transitions and hover effects
* Clinical AI dashboard styling

---

# System Architecture

```text
EEG File Upload
       ↓
Preprocessing Pipeline
       ↓
Connectivity Matrix Generation
       ↓
CNN + Attention Model
       ↓
Prediction + Confidence
       ↓
Patient History Storage
```

---

# AI Model

## Architecture

The prediction system uses:

* Convolutional Neural Networks (CNN)
* Attention Mechanism
* Subject-wise EEG analysis

## Why CNN + Attention?

### CNN

CNNs are highly effective for:

* Spatial feature extraction
* EEG pattern recognition
* Connectivity matrix analysis
* Noise robustness

### Attention Mechanism

Attention improves:

* Important region focus
* Signal relevance learning
* Better feature weighting
* Improved interpretability

The combination allows the model to learn both:

* Local EEG spatial patterns
* Global important neural relationships

---

# Tech Stack

## Frontend

* Next.js
* TypeScript
* Tailwind CSS
* NextAuth

## Backend

* Prisma ORM
* SQLite
* API Routes

## AI / Signal Processing

* Python
* PyTorch
* NumPy
* MNE

---

# Project Structure

```text
frontend/
 ├── app/
 │    ├── dashboard/
 │    ├── upload/
 │    ├── preprocess/
 │    ├── patients/
 │    ├── history/
 │    └── api/
 │
 ├── prisma/
 ├── lib/
 └── components/

models/
preprocessing/
results/
```

---

# Installation

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd eeg_ad
```

---

## 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## 3. Setup Python Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Setup Prisma

```bash
npx prisma generate
npx prisma db push
```

---

# Running the Project

## Start Frontend

```bash
cd frontend
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

# Workflow

1. Add Patient
2. Upload EEG File
3. Run Preprocessing
4. Generate Connectivity Matrix
5. Run AI Prediction
6. Store Prediction History
7. Review Results Dashboard

---

# Authentication

The platform uses:

* NextAuth authentication
* Protected dashboard routes
* Session-based access control

---

# Future Improvements

* Multi-class neurological disorder prediction
* Real-time EEG streaming
* Explainable AI visualizations
* Cloud deployment
* Multi-user support
* Advanced analytics dashboard
* Research reporting tools

---

# Project Goals

* Explore EEG-based AI diagnostics
* Improve neurological analysis workflows
* Build scalable clinical AI systems
* Research deep learning for brain signal analysis

---

# License

This project is developed for educational, research, and AI experimentation purposes.

---

# Author

Developed as part of an EEG-based deep learning research and full-stack AI platform project.
