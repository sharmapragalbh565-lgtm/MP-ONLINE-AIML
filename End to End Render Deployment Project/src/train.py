"""
src/train.py
Generates a synthetic car dataset and trains a Random Forest Regressor.
Saves the pipeline (preprocessor + model) to models/model.pkl.
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

# ─── Reproducibility ───────────────────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)

N = 8000  # number of synthetic training samples

# ─── Generate Synthetic Data ───────────────────────────────────────────────────
def generate_dataset(n: int) -> pd.DataFrame:
    """
    Creates a realistic synthetic car dataset.
    Pricing logic is grounded in real used-car market dynamics:
      - Newer cars retain more value
      - Diesel & Automatics command a premium
      - Higher mileage reduces value
      - More owners reduce value
    """
    car_age       = np.random.randint(1, 18, n)
    present_price = np.random.uniform(3.0, 35.0, n)          # ex-showroom price (Lakhs)
    kms_driven    = np.random.randint(5_000, 200_000, n)
    owner         = np.random.choice([0, 1, 2, 3], n, p=[0.50, 0.30, 0.15, 0.05])
    fuel_type     = np.random.choice(
        ["Petrol", "Diesel", "CNG", "Electric"], n, p=[0.45, 0.40, 0.08, 0.07]
    )
    seller_type   = np.random.choice(["Dealer", "Individual"], n, p=[0.55, 0.45])
    transmission  = np.random.choice(["Manual", "Automatic"], n, p=[0.60, 0.40])

    # ── Price construction (ground-truth label) ───────────────────────────────
    # Start from present price and depreciate
    depreciation_rate = 0.12 + 0.01 * car_age
    base_price = present_price * np.maximum(0.05, 1 - depreciation_rate * car_age * 0.08)

    # Mileage penalty
    mileage_factor = 1 - (kms_driven / 200_000) * 0.35

    # Owner penalty
    owner_factor = 1 - owner * 0.07

    # Fuel bonus
    fuel_bonus = np.where(
        fuel_type == "Diesel", 1.08,
        np.where(fuel_type == "Electric", 1.12,
        np.where(fuel_type == "CNG", 0.95, 1.0))
    )

    # Transmission bonus
    auto_bonus = np.where(transmission == "Automatic", 1.06, 1.0)

    # Seller premium (dealers slightly higher due to certification)
    seller_factor = np.where(seller_type == "Dealer", 1.04, 1.0)

    selling_price = (
        base_price
        * mileage_factor
        * owner_factor
        * fuel_bonus
        * auto_bonus
        * seller_factor
    )
    # Add realistic noise (±5%)
    selling_price *= np.random.normal(1.0, 0.05, n)
    selling_price  = np.clip(selling_price, 0.25, 80.0)

    return pd.DataFrame({
        "car_age":       car_age,
        "present_price": present_price,
        "kms_driven":    kms_driven,
        "owner":         owner,
        "fuel_type":     fuel_type,
        "seller_type":   seller_type,
        "transmission":  transmission,
        "selling_price": selling_price,
    })


# ─── Feature Definitions ───────────────────────────────────────────────────────
NUMERIC_FEATURES     = ["car_age", "present_price", "kms_driven", "owner"]
CATEGORICAL_FEATURES = ["fuel_type", "seller_type", "transmission"]
TARGET               = "selling_price"


def build_pipeline() -> Pipeline:
    """Construct the sklearn preprocessing + model pipeline."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    model = GradientBoostingRegressor(
        n_estimators=400,
        learning_rate=0.08,
        max_depth=5,
        subsample=0.85,
        random_state=SEED,
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def train():
    print("Generating synthetic dataset ...")
    df = generate_dataset(N)

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=SEED
    )

    print(f"Training on {len(X_train)} samples, evaluating on {len(X_test)} ...")
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    mae    = mean_absolute_error(y_test, y_pred)
    r2     = r2_score(y_test, y_pred)
    print(f"  [OK] MAE : {mae:.4f} Lakhs")
    print(f"  [OK] R2  : {r2:.4f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(pipeline, "models/model.pkl")
    print("  [OK] Model saved to models/model.pkl")


if __name__ == "__main__":
    train()
