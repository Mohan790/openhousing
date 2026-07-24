# OpenHousing — My Contribution

**Scope owned:** Proof of Concept (POC), ETL Pipeline, Machine Learning Model, REST API, Web Interface

This document covers the components I personally built for the OpenHousing project — an instant real estate valuation tool for the Housing Observatory use case.

---

## 1. Proof of Concept (`notebooks/poc.ipynb`)

Before building production code, I validated feasibility in a Jupyter notebook using the real Boston Housing dataset.

- **Source data:** [BostonHousing.csv](https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv) — 506 records, 13 features + target
- **Steps:** data load → exploratory analysis (correlation heatmap) → baseline model comparison (Linear Regression vs. Random Forest) → feature importance
- **Result:** Random Forest achieved R² ≈ 0.88, confirming the dataset carries enough signal to proceed to a production pipeline

---

## 2. ETL Pipeline (`etl/`)

A three-stage pipeline, chained by a single orchestrator script.

| File | Responsibility |
|---|---|
| `extract.py` | Downloads the raw dataset from the source URL, saves a local copy |
| `transform.py` | Handles missing values (median imputation), removes invalid rows, converts target to full USD (`price_usd = medv * 1000`), engineers one derived feature (`rooms_per_dis`) |
| `load.py` | Saves the cleaned dataset to `data/processed_housing.csv` |
| `pipeline.py` | Runs Extract → Transform → Load as a single command |

**Run it:**
```bash
cd etl
python pipeline.py
```

---

## 3. Machine Learning (`ml/train.py`)

- **Model:** Random Forest Regressor (`n_estimators=300`, `max_depth=10`)
- **Features (13):** `crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat`
- **Target:** `price_usd`
- **Split:** 80/20 train/test, `random_state=42`
- **Performance:**

  | Metric | Value |
  |---|---|
  | R² | 0.880 |
  | MAE | ~$2,076 |
  | RMSE | ~$2,964 |

- **Output:** trained model + feature list bundled and saved to `ml/model.pkl` via `joblib`

**Run it:**
```bash
cd ml
python train.py
```

---

## 4. REST API (`api/main.py`)

Built with **FastAPI**, loads the trained model once at startup and serves predictions.

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | API status check |
| `/health` | GET | Health check (uptime monitoring) |
| `/predict` | POST | Accepts 13 property/tract features, returns `predicted_price_usd` |
| `/docs` | GET | Auto-generated interactive Swagger UI |

Input validation is handled via Pydantic — malformed requests are rejected automatically before reaching the model.

**Run it:**
```bash
uvicorn api.main:app --reload --port 8001
```

---

## 5. Web Interface (`static/index.html`)

A live, real-time valuation UI served directly by the API at `/app/`:

- Form covering all 13 model inputs, grouped into **Property**, **Neighborhood**, and **Civic & Tax**
- Calls `/predict` automatically as the user edits fields (debounced), plus a manual "Update estimate" button
- Displays the result as a listing-style card with price, live stat strip, and the model's R² confidence

No separate frontend server needed — mounted directly on the FastAPI app via `StaticFiles`.

---

## How everything connects

```
extract.py -> transform.py -> load.py     (ETL: raw data -> processed_housing.csv)
                 |
             train.py                      (ML: processed_housing.csv -> model.pkl)
                 |
             api/main.py                   (loads model.pkl, serves /predict)
                 |
             static/index.html             (calls /predict, displays live result)
```

## Tech stack

Python 3.11 - pandas - scikit-learn - FastAPI - Uvicorn - joblib - vanilla HTML/CSS/JS (no frontend framework)

## Notes for the team

- Target currency is **USD**, converted from the source dataset's `medv` (in $1000s)
- No MLflow/Optuna/XGBoost/PostgreSQL — this implementation intentionally kept the stack minimal (CSV-based storage, Random Forest, no experiment tracking) to match project scope and timeline; flagging in case slides referencing those tools need to be reconciled with the actual codebase
