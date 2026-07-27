"""
app.py – Flask backend for the Car Value Predictor
"""

import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ─── Load Model ────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model.pkl")

try:
    pipeline = joblib.load(MODEL_PATH)
    print(f"[OK] Model loaded from {MODEL_PATH}")
except FileNotFoundError:
    pipeline = None
    print("[WARN] Model not found. Please run: python src/train.py")


# ─── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if pipeline is None:
        return jsonify({"error": "Model not trained yet. Run: python src/train.py"}), 503

    try:
        data = request.get_json(force=True)

        car_age       = int(data["car_age"])
        present_price = float(data["present_price"])
        kms_driven    = int(data["kms_driven"])
        owner         = int(data["owner"])
        fuel_type     = str(data["fuel_type"])
        seller_type   = str(data["seller_type"])
        transmission  = str(data["transmission"])

        # Basic validation
        if not (0 < car_age <= 30):
            raise ValueError("Car age must be between 1 and 30 years.")
        if not (0.1 <= present_price <= 150):
            raise ValueError("Present price must be between 0.1 and 150 Lakhs.")
        if not (0 <= kms_driven <= 500_000):
            raise ValueError("KMs driven must be between 0 and 500,000.")
        if owner not in [0, 1, 2, 3]:
            raise ValueError("Owner must be 0, 1, 2, or 3.")
        if fuel_type not in ["Petrol", "Diesel", "CNG", "Electric"]:
            raise ValueError("Invalid fuel type.")
        if seller_type not in ["Dealer", "Individual"]:
            raise ValueError("Invalid seller type.")
        if transmission not in ["Manual", "Automatic"]:
            raise ValueError("Invalid transmission type.")

        input_df = pd.DataFrame([{
            "car_age":       car_age,
            "present_price": present_price,
            "kms_driven":    kms_driven,
            "owner":         owner,
            "fuel_type":     fuel_type,
            "seller_type":   seller_type,
            "transmission":  transmission,
        }])

        prediction = pipeline.predict(input_df)[0]
        prediction = max(0.1, round(float(prediction), 2))

        # Confidence interval (±10%)
        lower = round(prediction * 0.90, 2)
        upper = round(prediction * 1.10, 2)

        return jsonify({
            "predicted_price": prediction,
            "lower_bound":     lower,
            "upper_bound":     upper,
            "currency":        "Lakhs (INR)",
        })

    except (KeyError, TypeError) as e:
        return jsonify({"error": f"Missing or invalid field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {e}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
