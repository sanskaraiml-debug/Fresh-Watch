import json

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

FEATURES = ["stock", "daily_sales", "days_left", "expected_sales", "leftover"]


def make_dataset(n=5000, seed=42):
    """Create a synthetic supermarket dataset."""
    np.random.seed(seed)
    stock = np.random.randint(5, 100, n)
    daily_sales = np.random.uniform(0.5, 10, n)
    days_left = np.random.randint(1, 31, n)

    expected_sales = daily_sales * days_left
    noise = np.random.normal(0, 10, n)
    wasted = (stock > expected_sales + noise).astype(int)

    df = pd.DataFrame({
        "stock": stock,
        "daily_sales": daily_sales.round(1),
        "days_left": days_left,
        "wasted": wasted,
    })

    # feature engineering: give the model the "multiplication" ready-made
    df["expected_sales"] = df["daily_sales"] * df["days_left"]
    df["leftover"] = df["stock"] - df["expected_sales"]
    return df


def train(save=True):
    df = make_dataset()
    X = df[FEATURES]
    y = df["wasted"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
        "Random Forest": RandomForestClassifier(
            random_state=42, min_samples_leaf=5
        ),
    }

    comparison = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        comparison.append({
            "model": name,
            "accuracy": round(accuracy_score(y_test, pred), 4),
            "precision": round(precision_score(y_test, pred), 4),
            "recall": round(recall_score(y_test, pred), 4),
            "f1": round(f1_score(y_test, pred), 4),
        })

    rf = models["Random Forest"]
    rf_pred = rf.predict(X_test)

    metrics = {
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "features": FEATURES,
        "comparison": comparison,
        "confusion_matrix": confusion_matrix(y_test, rf_pred).tolist(),
        "feature_importance": dict(
            zip(FEATURES, [round(float(v), 4) for v in rf.feature_importances_])
        ),
    }

    if save:
        df.to_csv("products.csv", index=False)
        joblib.dump(rf, "wastage_model.pkl")
        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

    return rf, metrics


if __name__ == "__main__":
    model, metrics = train(save=True)
    print("Dataset created:", metrics["train_rows"] + metrics["test_rows"], "rows")
    print()
    print(f"{'Model':22s}{'Accuracy':>10s}{'Precision':>11s}{'Recall':>9s}{'F1':>8s}")
    for m in metrics["comparison"]:
        print(f"{m['model']:22s}{m['accuracy']:>10.3f}{m['precision']:>11.3f}"
              f"{m['recall']:>9.3f}{m['f1']:>8.3f}")
    print()
    print("Model accuracy:", [m for m in metrics["comparison"]
                              if m["model"] == "Random Forest"][0]["accuracy"])
    print("Saved: wastage_model.pkl, metrics.json, products.csv")