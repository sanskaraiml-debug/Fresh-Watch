import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. create the dataset
np.random.seed(42)
n = 5000

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
    "wasted": wasted
})

# 2. feature engineering: give the model the "multiplication" ready-made
df["expected_sales"] = df["daily_sales"] * df["days_left"]
df["leftover"] = df["stock"] - df["expected_sales"]

# save the dataset as a file too
df.to_csv("products.csv", index=False)
print("Dataset created:", len(df), "rows")

# 3. train the model
FEATURES = ["stock", "daily_sales", "days_left", "expected_sales", "leftover"]
X = df[FEATURES]
y = df["wasted"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(random_state=42, min_samples_leaf=5)
model.fit(X_train, y_train)

# 4. check accuracy
accuracy = accuracy_score(y_test, model.predict(X_test))
print("Model accuracy:", accuracy)

# 5. save the trained model
joblib.dump(model, "wastage_model.pkl")
print("Model saved as wastage_model.pkl")
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 3. check accuracy
accuracy = accuracy_score(y_test, model.predict(X_test))
print("Model accuracy:", accuracy)

# 4. save the trained model
joblib.dump(model, "wastage_model.pkl")
print("Model saved as wastage_model.pkl")