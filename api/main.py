# ── Layer 1: imports + load model ──
import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "model.pkl")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

app = FastAPI(
    title="OpenHousing Price Prediction API",
    description="Predicts real estate price (USD) based on the Boston Housing indicators.",
    version="1.0.0",
)

app.mount("/app", StaticFiles(directory=STATIC_DIR, html=True), name="static")

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
FEATURES = bundle["features"]


# ── Layer 2: define input schema ──
class HousingFeatures(BaseModel):
    crim: float = Field(..., example=0.1)
    zn: float = Field(..., example=18.0)
    indus: float = Field(..., example=2.3)
    chas: int = Field(..., example=0)
    nox: float = Field(..., example=0.5)
    rm: float = Field(..., example=6.5)
    age: float = Field(..., example=65.0)
    dis: float = Field(..., example=4.0)
    rad: int = Field(..., example=1)
    tax: int = Field(..., example=296)
    ptratio: float = Field(..., example=15.3)
    b: float = Field(..., example=396.9)
    lstat: float = Field(..., example=5.0)


# ── Layer 3: define endpoints ──
@app.get("/")
def root():
    return {"status": "ok", "message": "OpenHousing API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(features: HousingFeatures):
    df = pd.DataFrame([features.dict()])[FEATURES]
    prediction = model.predict(df)[0]
    return {"predicted_price_usd": round(float(prediction), 2)}