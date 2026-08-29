"""
AgriVision backend — FastAPI service that accepts agricultural CSV
uploads, runs analysis, generates charts + a PDF report, and serves it
all to the React frontend.

Run with:
    python -m uvicorn backend.main:app --reload
(from the project root, so the `backend` package resolves)
"""

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import database, processing

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "storage" / "uploads"
CHARTS_DIR = BASE_DIR / "storage" / "charts"
REPORTS_DIR = BASE_DIR / "storage" / "reports"

for d in (UPLOAD_DIR, CHARTS_DIR, REPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

database.init_db()

app = FastAPI(title="AgriVision API", version="1.0.0")

# Dev-friendly CORS: the Vite dev server runs on a different port than
# uvicorn, so the frontend needs cross-origin access to the API and to
# the static chart/report files below.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/charts", StaticFiles(directory=CHARTS_DIR), name="charts")
app.mount("/report", StaticFiles(directory=REPORTS_DIR), name="report")


# ---------------------------------------------------------------- health --
@app.get("/api/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------- upload --
@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    dest_path = UPLOAD_DIR / file.filename
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    with open(dest_path, "wb") as f:
        f.write(contents)

    try:
        df = pd.read_csv(dest_path)
    except Exception as exc:  # malformed CSV, bad encoding, etc.
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {exc}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Dataset has no rows.")

    analysis = processing.analyze_dataset(df)

    # Insert first (without charts/report) to obtain the dataset id used
    # to namespace generated chart files, then patch the row afterward.
    dataset_id = database.insert_dataset(
        {
            "filename": file.filename,
            "upload_date": datetime.now(timezone.utc).isoformat(),
            "file_path": str(dest_path),
            "rows": analysis["rows"],
            "columns": analysis["columns"],
            "missing_values": analysis["missing_values"],
            "duplicate_rows": analysis["duplicate_rows"],
            "outliers": analysis["outliers"],
            "stats": analysis,
            "charts": {},
            "report": None,
        }
    )

    charts = processing.generate_charts(df, dataset_id, CHARTS_DIR)
    report_path = processing.generate_report(
        df, analysis, dataset_id, file.filename, CHARTS_DIR, REPORTS_DIR
    )

    # Patch the row with charts + report now that they exist.
    conn = database.get_connection()
    import json as _json

    conn.execute(
        "UPDATE datasets SET charts_json = ?, report = ? WHERE id = ?",
        (_json.dumps(charts), report_path, dataset_id),
    )
    conn.commit()
    conn.close()

    return {
        "id": dataset_id,
        "filename": file.filename,
        "rows": analysis["rows"],
        "columns": analysis["columns"],
        "charts": charts,
        "report": report_path,
    }


# -------------------------------------------------------------- datasets --
@app.get("/api/datasets")
def get_datasets():
    return database.list_datasets()


@app.get("/api/datasets/{dataset_id}")
def get_dataset(dataset_id: int):
    dataset = database.get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    return dataset


@app.get("/api/datasets/{dataset_id}/columns")
def get_dataset_columns(dataset_id: int):
    dataset = database.get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    stats = dataset["stats"]
    return {
        "numeric_columns": stats.get("numeric_columns", []),
        "categorical_columns": stats.get("categorical_columns", []),
    }


# -------------------------------------------------------------- analysis --
@app.get("/api/analysis/{dataset_id}")
def get_analysis(dataset_id: int):
    dataset = database.get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    return {
        "id": dataset["id"],
        "filename": dataset["filename"],
        "upload_date": dataset["upload_date"],
        "rows": dataset["rows"],
        "columns": dataset["columns"],
        "missing_values": dataset["missing_values"],
        "duplicate_rows": dataset["duplicate_rows"],
        "outliers": dataset["outliers"],
        "stats": dataset["stats"],
        "charts": dataset["charts"],
        "report": dataset["report"],
    }


# ------------------------------------------------------------- prediction --
class PredictRequest(BaseModel):
    dataset_id: int
    target_column: str
    features: dict


@app.post("/api/predict")
def predict(req: PredictRequest):
    dataset = database.get_dataset(req.dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    file_path = dataset["file_path"]
    try:
        df = pd.read_csv(file_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not reload dataset: {exc}")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if req.target_column not in numeric_cols:
        raise HTTPException(
            status_code=400, detail="Target column must be a numeric column."
        )
    feature_cols = [c for c in numeric_cols if c != req.target_column]
    if not feature_cols:
        raise HTTPException(
            status_code=400, detail="Dataset needs at least one other numeric column."
        )

    working = df[feature_cols + [req.target_column]].dropna()
    if len(working) < 5:
        raise HTTPException(
            status_code=400, detail="Not enough complete rows to fit a model."
        )

    X = working[feature_cols].values.astype(float)
    y = working[req.target_column].values.astype(float)
    X_design = np.column_stack([np.ones(len(X)), X])

    coeffs, *_ = np.linalg.lstsq(X_design, y, rcond=None)
    predictions = X_design @ coeffs
    ss_res = float(np.sum((y - predictions) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    try:
        input_vector = [1.0] + [float(req.features[c]) for c in feature_cols]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Missing feature value: {exc}")
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Feature values must be numeric.")

    predicted_value = float(np.dot(coeffs, input_vector))

    return {
        "target_column": req.target_column,
        "predicted_value": predicted_value,
        "features_used": feature_cols,
        "r_squared": round(r_squared, 4),
        "sample_size": int(len(working)),
    }
