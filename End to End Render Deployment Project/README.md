<div align="center">

# 🔍 CarLens AI

### ML-Powered Used Car Resale Price Estimator

*Predict the resale value of any used car instantly using a trained Gradient Boosting model.*

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

---

## Overview

**CarLens AI** is a full-stack machine learning web application that predicts the resale market value of a used car based on 7 key parameters. It combines a Gradient Boosting Regressor backend with a glassmorphism dark-mode UI, and supports both INR and USD currency modes as well as km and miles distance input.

---

## Features

| Feature | Details |
|---|---|
| **ML Model** | Gradient Boosting Regressor · R² ≈ 0.98 · MAE ≈ 0.61 Lakhs |
| **Dual Currency** | INR (Lakhs) ↔ USD with live conversion (1 USD = 84 INR) |
| **Dual Distance** | km ↔ miles with automatic conversion before inference |
| **Glassmorphism UI** | Black & crystal-white theme · frosted glass inputs · animated orbs |
| **Glowing Unit Badges** | `Lakhs` · `Years` · `km` pulse inside each input field |
| **Animated Result** | Price counter animates on prediction with a confidence range bar |
| **REST API** | Flask `/predict` endpoint with full server-side validation |

---

## Tech Stack

```
Backend   →  Python · Flask · scikit-learn · pandas · numpy · joblib
Frontend  →  Vanilla HTML5 · CSS3 (glassmorphism) · JavaScript (ES6+)
Container →  Docker
```

---

## Project Structure

```
CarLens/
├── models/                  # Auto-generated ML artifacts
│   └── model.pkl            # Trained GradientBoosting pipeline
│
├── src/
│   └── train.py             # Synthetic dataset generation + model training
│
├── static/
│   ├── css/
│   │   └── style.css        # Glassmorphism dark theme
│   └── js/
│       └── app.js           # Unit conversion + async prediction logic
│
├── templates/
│   └── index.html           # Main UI (form + result panel)
│
├── app.py                   # Flask REST API server
├── Dockerfile               # Container build definition
├── .dockerignore            # Docker build exclusions
├── .gitignore               # Git exclusions
└── requirements.txt         # Python dependencies
```

---

## Local Setup

> **Prerequisites:** Python 3.9+ · pip

```bash
# 1. Clone the repository
git clone https://github.com/sharmapragalbh565-lgtm/CarLens.git
cd CarLens

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model  →  generates models/model.pkl
python src/train.py

# 4. Start the development server
python app.py
```

Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## Docker

The `Dockerfile` provides a fully self-contained container — it installs all dependencies **and trains the model** at build time, so no pre-built `.pkl` file is needed.

### Dockerfile Overview

```dockerfile
FROM python:3.11-slim          # Lightweight base image
WORKDIR /app                   # Set working directory
COPY requirements.txt .        # Copy and install deps first (layer cache)
RUN pip install --no-cache-dir -r requirements.txt
COPY . .                       # Copy all project files
RUN python src/train.py        # Train model at build time
EXPOSE 5000                    # Expose Flask port
CMD ["python", "app.py"]       # Start the server
```

### Build & Run

```bash
# Build the image (trains the model inside Docker)
docker build -t carlens .

# Run the container
docker run -p 5000:5000 carlens
```

Then open **[http://localhost:5000](http://localhost:5000)**.

### Useful Docker Commands

```bash
# Run in detached (background) mode
docker run -d -p 5000:5000 --name carlens-app carlens

# View container logs
docker logs carlens-app

# Stop the container
docker stop carlens-app

# Remove the container
docker rm carlens-app
```

---

## API Reference

### `POST /predict`

Accepts a JSON body and returns the estimated resale value.

**Request**
```json
{
  "present_price": 8.5,
  "car_age": 4,
  "kms_driven": 45000,
  "owner": 0,
  "fuel_type": "Diesel",
  "seller_type": "Dealer",
  "transmission": "Automatic"
}
```

**Response**
```json
{
  "predicted_price": 5.42,
  "lower_bound": 4.88,
  "upper_bound": 5.96,
  "currency": "Lakhs (INR)"
}
```

> All values are in **Lakhs INR**. Unit conversion (miles → km, USD → Lakhs) is handled client-side before the request is sent.

---

## How the Model Works

### Input Features

| Feature | Type | Description |
|---|---|---|
| `present_price` | Float | Ex-showroom price in Lakhs INR |
| `car_age` | Integer | Years since manufacture |
| `kms_driven` | Integer | Total kilometres driven |
| `owner` | Integer | 0 = first owner · 3 = fourth+ owner |
| `fuel_type` | Categorical | Petrol / Diesel / CNG / Electric |
| `seller_type` | Categorical | Dealer / Individual |
| `transmission` | Categorical | Manual / Automatic |

### Pipeline

```
Raw Input  →  ColumnTransformer  →  GradientBoostingRegressor  →  Price (Lakhs)
               ├── StandardScaler    (numerical features)
               └── OneHotEncoder     (categorical features)
```

### Training Stats
- **Dataset:** 8,000 synthetic records
- **Train / Test split:** 85% / 15%
- **R² Score:** ~0.985
- **MAE:** ~0.61 Lakhs

### Unit Conversions
```
Miles  →  km       :  km     = miles × 1.60934
USD    →  Lakhs    :  lakhs  = (USD × 84) / 100,000
Lakhs  →  USD      :  USD    = lakhs × 100,000 / 84
```

---

## Deployment — Render

CarLens AI can be deployed for free on **[Render](https://render.com)** directly from the GitHub repository. The `render.yaml` Blueprint handles everything automatically.

### How it works

```yaml
# render.yaml
services:
  - type: web
    name: carlens-ai
    runtime: python
    plan: free
    buildCommand: "pip install -r requirements.txt && python src/train.py"
    startCommand: "gunicorn app:app"
```

| Step | What happens |
|---|---|
| **Build** | Installs all Python dependencies from `requirements.txt` |
| **Train** | Runs `src/train.py` — generates `models/model.pkl` inside the container |
| **Start** | Serves the app via `gunicorn` (production WSGI server) on the PORT Render assigns |

### Steps

1. **Push** the repo to GitHub (including `render.yaml`)
2. Go to **[dashboard.render.com](https://dashboard.render.com)** → **New → Web Service**
3. Connect your GitHub account and select the **CarLens** repository
4. Render auto-detects `render.yaml` — click **Deploy**
5. Wait ~2–3 minutes for the build to finish
6. Your live URL will be: `https://carlensapp.onrender.com`

> **Free tier note:** Render's free plan spins down the service after 15 minutes of inactivity. The first request after sleep may take ~30 seconds to wake up.

---

## License

MIT — free to use, modify, and distribute.