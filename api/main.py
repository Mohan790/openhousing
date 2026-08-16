"""OpenHousing REST API — built by Mohan790."""

import os
import joblib
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "model.pkl")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

# --- Rate limiter setup ---
# Limits requests per client IP address. Applied per-endpoint below.
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="OpenHousing Price Prediction API",
    description="Predicts real estate price (USD) based on the Boston Housing indicators.",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Serves the web page (static/index.html) at http://.../app
app.mount("/app", StaticFiles(directory=STATIC_DIR, html=True), name="static")

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
FEATURES = bundle["features"]


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


@app.get("/")
def root():
    return {"status": "ok", "message": "OpenHousing API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
@limiter.limit("10/minute")  # max 10 requests per minute, per IP address
def predict(request: Request, features: HousingFeatures):
    df = pd.DataFrame([features.dict()])[FEATURES]
    prediction = model.predict(df)[0]
    return {"predicted_price_usd": round(float(prediction), 2)}