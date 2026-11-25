import json
import os
import sys
from typing import List, Optional
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Inventory Analysis ML Microservice",
    description="Machine Learning Service exposing trained Random Forest expiry prediction models for Inventory Analysis",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths to model and metrics
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "wastage_model.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "metrics.json")

model = None
metrics = {}

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"[+] Loaded ML model from {MODEL_PATH}")
    else:
        print(f"[!] Warning: Model not found at {MODEL_PATH}")

    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)
        print(f"[+] Loaded evaluation metrics from {METRICS_PATH}")
    else:
        print(f"[!] Warning: Metrics not found at {METRICS_PATH}")
except Exception as e:
    print(f"[!] Error loading model or metrics: {e}")


class ItemPredictRequest(BaseModel):
    product: str = Field(..., example="Fresh Cow Milk (1L)")
    stock: float = Field(..., ge=0, example=24.0)
    daily_sales: float = Field(..., ge=0, example=3.0)
    days_left: int = Field(..., ge=0, example=3)
    price: Optional[float] = Field(default=0.0, ge=0, example=32.0)
    category: Optional[str] = Field(default="General", example="Dairy")


class BatchPredictRequest(BaseModel):
    items: List[ItemPredictRequest]


def compute_prediction(req: ItemPredictRequest) -> dict:
    stock = float(req.stock)
    daily_sales = float(req.daily_sales)
    days_left = int(req.days_left)
    price = float(req.price or 0.0)

    expected_sales = daily_sales * days_left
    leftover = stock - expected_sales
    features = np.array([[stock, daily_sales, days_left, expected_sales, leftover]])

    if model is not None:
        try:
            prob_arr = model.predict_proba(features)
            wastage_chance = float(np.round(prob_arr[0][1] * 100, 1))
        except Exception:
            # Fallback mathematical model if sklearn version mismatch
            ratio = leftover / max(stock, 1.0)
            wastage_chance = float(np.clip(ratio * 100, 0, 100))
    else:
        ratio = leftover / max(stock, 1.0)
        wastage_chance = float(np.clip(ratio * 100, 0, 100))

    if wastage_chance >= 75.0:
        risk_level = "High Risk"
    elif wastage_chance >= 45.0:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    unsold_quantity = max(float(np.round(leftover, 1)), 0.0)
    potential_loss = float(np.round(unsold_quantity * price, 2))

    # Prescriptive recommendation logic
    if risk_level == "High Risk":
        if days_left <= 3:
            discount_pct = 40
            action = "Give a 40% liquidation discount or execute return to supplier today"
        elif days_left <= 7:
            discount_pct = 25
            action = "Apply a 20-30% discount or create a promotional combo offer"
        else:
            discount_pct = 15
            action = "Move to eye-level front shelf and apply a 10-15% markdown"
    elif risk_level == "Medium Risk":
        discount_pct = 10
        action = "Keep under close watch; feature in weekly specials"
    else:
        discount_pct = 0
        action = "Healthy sales velocity; maintain standard retail pricing"

    suggested_price = float(np.round(price * (1.0 - (discount_pct / 100.0)), 2))

    return {
        "product": req.product,
        "category": req.category,
        "stock": stock,
        "daily_sales": daily_sales,
        "days_left": days_left,
        "price": price,
        "expected_sales": float(np.round(expected_sales, 1)),
        "unsold_quantity": unsold_quantity,
        "potential_loss": potential_loss,
        "wastage_chance": wastage_chance,
        "risk_level": risk_level,
        "discount_pct": discount_pct,
        "suggested_price": suggested_price,
        "recommended_action": action,
    }


@app.get("/")
def root():
    return {
        "name": "Inventory Analysis ML Prediction Microservice",
        "status": "online",
        "model_loaded": model is not None,
        "endpoints": ["/health", "/model-info", "/predict", "/batch-predict"],
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "features": metrics.get("features", ["stock", "daily_sales", "days_left", "expected_sales", "leftover"]),
    }


@app.get("/model-info")
def model_info():
    return {
        "model_type": "Random Forest Classifier",
        "estimators": 100,
        "features": metrics.get("features", []),
        "training_samples": metrics.get("train_rows", 4000),
        "testing_samples": metrics.get("test_rows", 1000),
        "comparison": metrics.get("comparison", []),
        "confusion_matrix": metrics.get("confusion_matrix", []),
        "feature_importance": metrics.get("feature_importance", {}),
    }


@app.post("/predict")
def predict_single(req: ItemPredictRequest):
    return compute_prediction(req)


@app.post("/batch-predict")
def predict_batch(req: BatchPredictRequest):
    results = [compute_prediction(item) for item in req.items]
    high_count = sum(1 for r in results if r["risk_level"] == "High Risk")
    med_count = sum(1 for r in results if r["risk_level"] == "Medium Risk")
    low_count = sum(1 for r in results if r["risk_level"] == "Low Risk")
    total_loss = sum(r["potential_loss"] for r in results)

    return {
        "total_items": len(results),
        "high_risk_count": high_count,
        "medium_risk_count": med_count,
        "low_risk_count": low_count,
        "total_potential_loss": float(np.round(total_loss, 2)),
        "predictions": results,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
