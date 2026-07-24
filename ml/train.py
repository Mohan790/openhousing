import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

PROCESSED_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed_housing.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

FEATURES = [
    "crim", "zn", "indus", "chas", "nox", "rm", "age",
    "dis", "rad", "tax", "ptratio", "b", "lstat",
]
TARGET = "price_usd"


def train_model():
    df = pd.read_csv(PROCESSED_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=300, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = mean_squared_error(y_test, preds) ** 0.5
    r2 = r2_score(y_test, preds)

    print(f"[train] MAE: ${mae:,.2f}")
    print(f"[train] RMSE: ${rmse:,.2f}")
    print(f"[train] R2 score: {r2:.3f}")

    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)
    print(f"[train] model saved to {MODEL_PATH}")

    return {"mae": mae, "rmse": rmse, "r2": r2}


if __name__ == "__main__":
    train_model()