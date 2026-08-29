"""
database.py — lightweight SQLite persistence layer for AgriVision.

Stores one row per uploaded dataset: identifying info, computed analysis
summary (as JSON), the chart path map (as JSON), and the report path.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "agrivision.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            file_path TEXT NOT NULL,
            rows INTEGER NOT NULL,
            columns INTEGER NOT NULL,
            missing_values INTEGER NOT NULL,
            duplicate_rows INTEGER NOT NULL,
            outliers INTEGER NOT NULL,
            stats_json TEXT NOT NULL,
            charts_json TEXT NOT NULL,
            report TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def insert_dataset(record: dict) -> int:
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO datasets
            (filename, upload_date, file_path, rows, columns,
             missing_values, duplicate_rows, outliers, stats_json,
             charts_json, report)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["filename"],
            record.get("upload_date") or datetime.now(timezone.utc).isoformat(),
            record["file_path"],
            record["rows"],
            record["columns"],
            record["missing_values"],
            record["duplicate_rows"],
            record["outliers"],
            json.dumps(record["stats"]),
            json.dumps(record["charts"]),
            record.get("report"),
        ),
    )
    conn.commit()
    dataset_id = cur.lastrowid
    conn.close()
    return dataset_id


def list_datasets() -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, filename, upload_date, rows, columns, missing_values, "
        "duplicate_rows, outliers FROM datasets ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dataset(dataset_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM datasets WHERE id = ?", (dataset_id,)
    ).fetchone()
    conn.close()
    if row is None:
        return None
    data = dict(row)
    data["stats"] = json.loads(data.pop("stats_json"))
    data["charts"] = json.loads(data.pop("charts_json"))
    return data
