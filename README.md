# Deep Learning-Based Fingerprint Analysis for Gender and Blood Group Classification in Forensic Applications
[Kindly check final_review folder for the ppt , video demo and results] 

WEBSIT--> https://forensic-prediction.vercel.app/
PAPER-->https://digital-library.theiet.org/doi/10.1049/icp.2025.4755


## Overview

This project presents a deep learning–based forensic profiling system capable of predicting gender and blood group information directly from fingerprint images. The system integrates Computer Vision, Convolutional Neural Networks (CNNs), Transfer Learning, and Explainable Artificial Intelligence (XAI) techniques to extract meaningful biometric patterns from fingerprints for forensic applications.

Traditional fingerprint systems primarily rely on minutiae-based matching techniques for identity verification. However, these systems become ineffective when the fingerprint does not exist in a criminal or biometric database. This project addresses that limitation by introducing a soft biometric profiling approach capable of inferring demographic attributes directly from fingerprint ridge structures.

The proposed system predicts:

- Gender (Male / Female)
- Blood Group (A+, A−, B+, B−, AB+, AB−, O+, O−)

The architecture follows a distributed client–server model where:
- Frontend is deployed on Vercel
- Backend API is deployed on Railway
- Deep learning inference is performed using TensorFlow/Keras
- Image preprocessing is implemented using OpenCV

---

# Problem Statement

The objective of this project is to design and implement a deep learning–based forensic profiling system capable of predicting gender and blood group from fingerprint images in scenarios where direct fingerprint matching is unavailable or ineffective.

The system aims to assist forensic investigations by extracting soft biometric information from latent fingerprints using advanced deep learning methodologies.

---

# Objectives

The primary objectives of this project are:

- To develop a fingerprint-based gender classification system using EfficientNetB0 transfer learning architecture.
- To design and train a custom CNN architecture for blood group prediction.
- To enhance fingerprint ridge-valley structures using CLAHE-based preprocessing techniques.
- To integrate Explainable AI using Grad-CAM for prediction interpretability.
- To build a scalable web-based forensic profiling application using a client–server architecture.
- To improve forensic investigation support in situations where traditional fingerprint databases fail.

---

# Key Features

## Fingerprint-Based Gender Classification

The system predicts the gender of an individual using fingerprint ridge density, texture distribution, and spatial orientation patterns extracted through deep learning feature representations.

---

## Fingerprint-Based Blood Group Prediction

A custom-designed Convolutional Neural Network predicts one of the eight blood group classes directly from fingerprint images.

---

## Explainable Artificial Intelligence (Grad-CAM)

Gradient-weighted Class Activation Mapping (Grad-CAM) is integrated to visualize the fingerprint regions contributing to predictions. This improves model transparency and forensic interpretability.

---

## CLAHE-Based Fingerprint Enhancement

Contrast Limited Adaptive Histogram Equalization (CLAHE) improves ridge-valley contrast and enhances low-quality fingerprint structures before inference.

---

## Distributed Frontend–Backend Deployment

The frontend and backend are independently deployed for:
- Scalability
- Maintainability
- Lightweight frontend delivery
- Faster API response handling

---

## REST API-Based Inference System

Prediction requests are processed through Flask REST APIs using multipart/form-data image uploads and JSON-based responses.

---

# System Architecture

The application follows a distributed frontend-backend architecture.

## High-Level Data Flow

```text
Client Browser (Frontend - Vercel)
            │
            ▼
Flask REST API (Backend - Railway)
            │
            ▼
Image Preprocessing Pipeline
            │
            ▼
Deep Learning Inference Engine
            │
            ▼
Prediction Processing
            │
            ▼
JSON Response Generation
```

---

# Detailed System Architecture

```text
Fingerprint Biometric Prediction System
(Client–Server Architecture)

┌────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (CLIENT)                               │
│                     HTML, CSS, JavaScript (Vercel)                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  User Interface                                                            │
│  ├── File Upload Module                                                    │
│  │     • Upload fingerprint image                                          │
│  │     • Supports JPG, JPEG, PNG, BMP                                     │
│  │                                                                         │
│  ├── Image Preview Module                                                  │
│  │     • Displays uploaded image                                           │
│  │                                                                         │
│  ├── Confidence Threshold Control                                          │
│  │     • Slider/Input threshold control                                    │
│  │                                                                         │
│  ├── Prediction Result Display                                             │
│  │     • Gender prediction                                                 │
│  │     • Blood group prediction                                            │
│  │     • Probability scores                                                │
│  │     • Confidence metrics                                                │
│  │                                                                         │
│  └── Client-Side Validation                                                │
│        • File type validation                                              │
│        • File size validation                                              │
│        • User notifications                                                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP POST Request
                                │ (Image + Threshold)
                                ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                       BACKEND SERVER (FLASK API)                           │
│                            Hosted on Railway                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. Request Handler Module                                                 │
│  ├── API Endpoints                                                         │
│  │     • /api/health                                                       │
│  │     • /api/predict                                                      │
│  │                                                                         │
│  └── Request Parsing and Validation                                        │
│                                                                            │
│  2. Image Preprocessing Module                                             │
│  ├── Grayscale Conversion                                                  │
│  ├── CLAHE Histogram Equalization                                          │
│  ├── Image Resizing                                                        │
│  │     • 224×224 (Gender Model)                                            │
│  │     • 150×150 (Blood Group Model)                                       │
│  ├── Normalization                                                         │
│  ├── Morphological Operations                                              │
│  └── Noise Reduction                                                       │
│                                                                            │
│  3. Model Loader Module                                                    │
│  ├── Load Models at Startup                                                │
│  ├── Cache Models in Memory                                                │
│  └── Fallback Recompilation                                                │
│                                                                            │
│  4. Prediction Module                                                      │
│  ├── Gender Classification Model                                           │
│  │     • EfficientNetB0                                                    │
│  │     • Binary Classification                                             │
│  │                                                                         │
│  └── Blood Group Classification Model                                      │
│        • Custom CNN                                                        │
│        • Multi-Class Classification                                        │
│                                                                            │
│  5. Result Processing Module                                               │
│  ├── Probability Computation                                               │
│  ├── Final Label Selection                                                 │
│  ├── Confidence Score Calculation                                          │
│  └── JSON Response Generation                                              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                             MODEL STORAGE                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  • EfficientNetB0 Gender Model (.keras / .h5)                              │
│  • Custom CNN Blood Group Model (.keras / .h5)                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

# Technology Stack

## Frontend Technologies

| Technology | Purpose |
|---|---|
| HTML5 | User Interface Structure |
| CSS3 | Styling and Layout |
| JavaScript | Client-Side Interactions |
| Fetch API | API Communication |
| Vercel | Frontend Deployment |

---

## Backend Technologies

| Technology | Purpose |
|---|---|
| Flask | REST API Backend |
| Flask-CORS | Cross-Origin Communication |
| Gunicorn | Production WSGI Server |
| Railway | Backend Deployment |

---

## Artificial Intelligence and Deep Learning

| Technology | Purpose |
|---|---|
| TensorFlow | Deep Learning Framework |
| Keras | Model Development |
| EfficientNetB0 | Gender Classification |
| Custom CNN | Blood Group Classification |

---

## Computer Vision and Image Processing

| Technology | Purpose |
|---|---|
| OpenCV | Image Processing |
| Pillow (PIL) | Image Handling |
| NumPy | Numerical Operations |

---

# Deep Learning Models

## Gender Classification Model

### Architecture
- EfficientNetB0
- Transfer Learning–based CNN
- Binary Classification

### Input Configuration
- Image Size: 224 × 224
- Grayscale Input

### Training Configuration
- Optimizer: Adam
- Loss Function: Binary Cross-Entropy
- Transfer Learning + Fine-Tuning

### Output Classes
- Male
- Female

### Model Performance
- Accuracy: ~90.13%

---

## Blood Group Classification Model

### Architecture
- Custom Convolutional Neural Network
- Multi-Class Classification

### Input Configuration
- Image Size: 150 × 150 × 3

### Output Classes

| Class Index | Blood Group |
|---|---|
| 0 | A+ |
| 1 | A− |
| 2 | B+ |
| 3 | B− |
| 4 | AB+ |
| 5 | AB− |
| 6 | O+ |
| 7 | O− |

### Training Configuration
- Optimizer: Adam
- Loss Function: Categorical Cross-Entropy
- Softmax Output Layer

### Model Performance
- Accuracy: ~90.60%

---

# Image Preprocessing Pipeline

The preprocessing stage is critical for improving ridge visibility and model performance.

## Preprocessing Operations

### 1. Grayscale Conversion
Converts RGB images into grayscale representations.

### 2. CLAHE Enhancement
Enhances local contrast and ridge-valley visibility.

### 3. Histogram Equalization
Improves fingerprint structural clarity.

### 4. Morphological Operations
Used for:
- Ridge enhancement
- Gap filling
- Noise removal

Operations include:
- Morphological Opening
- Morphological Closing

### 5. Median Filtering
Removes salt-and-pepper noise while preserving ridge structures.

### 6. Image Resizing
- 224×224 for EfficientNetB0
- 150×150 for Custom CNN

### 7. Normalization
Pixel values normalized to [0,1].

---

# Explainable AI using Grad-CAM

Gradient-weighted Class Activation Mapping (Grad-CAM) visualizes the fingerprint regions contributing to predictions.

The visualization focuses on:
- Ridge density
- Ridge continuity
- Ridge orientation
- Structural fingerprint patterns

Benefits:
- Improved interpretability
- Better forensic transparency
- Validation of biologically relevant features

---

# API Workflow

## API Endpoint

```http
POST /api/predict
```

## Request Type

```http
multipart/form-data
```

## Workflow

1. User uploads fingerprint image
2. Frontend sends HTTP POST request
3. Backend validates request
4. Fingerprint preprocessing executes
5. Deep learning inference runs
6. Confidence scores are computed
7. JSON response is generated

---

# Example JSON Response

```json
{
  "gender": "Female",
  "gender_confidence": 94.2,
  "blood_group": "AB+",
  "blood_group_confidence": 89.1
}
```

---

# Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
│
├── models/
│   ├── gender_model.keras
│   ├── blood_group_model.keras
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── templates/
│   └── index.html
│
├── utils/
│   ├── preprocessing.py
│   ├── prediction.py
│   ├── gradcam.py
│
├── uploads/
│
└── README.md
```

---

# Installation and Setup

## Clone Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```txt
Flask==2.3.3
flask-cors==4.0.1
numpy==1.26.4
opencv-python-headless==4.10.0.84
Pillow==12.2.0
tensorflow-cpu==2.21.0
scikit-learn==1.7.2
joblib==1.4.0
gunicorn==22.0.0
huggingface_hub==0.27.1
```

---

# Running the Application

```bash
python app.py
```

Local Server:

```text
http://127.0.0.1:5000
```

---

# Deployment

## Frontend
- Platform: Vercel

## Backend
- Platform: Railway

## Production WSGI Server
- Gunicorn

---

# Security Features

The system incorporates multiple security mechanisms:

- HTTPS encrypted communication
- CORS protection
- File validation mechanisms
- Temporary in-memory image processing
- Controlled API access
- No permanent biometric data storage

---

# Performance Metrics

| Model | Accuracy |
|---|---|
| EfficientNetB0 (Gender Classification) | 90.13% |
| Custom CNN (Blood Group Classification) | 90.60% |

Evaluation Metrics:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

---

# Datasets Used

## Gender Classification Dataset
- SOCOFing Dataset

## Blood Group Classification Dataset
- Kaggle Fingerprint Blood Group Dataset
- Primary fingerprint samples collected under ethical compliance

---

# Future Scope

Potential future enhancements include:

- Age prediction from fingerprints
- Real-time scanner integration
- Mobile application deployment
- Multi-modal biometric systems
- Federated learning implementation
- Advanced Explainable AI modules
- Fingerprint matching integration

---

# Research Contribution

This project contributes toward:
- AI-assisted forensic profiling
- Non-invasive biometric prediction
- Explainable forensic AI systems
- Deep learning applications in dermatoglyphics

The proposed system demonstrates how deep learning can assist forensic investigations when traditional fingerprint matching approaches fail.

---

# Authors

- Rajeshwari Golande
- Sukanya Bhaskar
- Yash Jahagirdar
- Rohit Kandelkar

---

# Acknowledgements

Special thanks to:

- Prof. Anandkumar Birajdar (Project Mentor)
- Dr. Rachana Patil (Head of Department)
- Rohit Kandelkar
- Yash Jahagirdar
- Sukanya Bhaskar

for their continuous support, guidance, technical contributions, and encouragement throughout the development of this project.

---

# Contact Information

For academic collaboration, technical discussions, or research inquiries:

- rajeshwari.golande22@pccoepune.org
- rajeshwarigolande143@gmail.com

---

# Academic Information

Bachelor of Technology (B.Tech)

Department of Computer Engineering (Regional Language)

Pimpri Chinchwad College of Engineering (PCCOE)

Pune, Maharashtra, India

Academic Year: 2025–2026

---

# Disclaimer

This project is developed strictly for educational, academic, and research purposes.

The predictions generated by the models are probabilistic estimations and should not be considered definitive forensic or medical evidence.

---

# License

This repository is intended for academic and research purposes only.
