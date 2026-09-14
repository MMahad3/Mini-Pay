import os
from typing import Any

import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://minipay:minipay@minipay-db.minipay.svc.cluster.local:5432/minipay")
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="MiniPay API")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "database": "ok"}
    except Exception as exc:  # pragma: no cover - for demo health endpoint
        raise HTTPException(status_code=503, detail={"status": "degraded", "database": str(exc)}) from exc


@app.get("/api/payments")
def list_payments() -> dict[str, Any]:
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            rows = conn.execute(
                "SELECT transaction_ref, amount, status, created_at FROM transactions ORDER BY created_at DESC LIMIT 10"
            ).fetchall()
        return {
            "items": [
                {
                    "transaction_ref": row[0],
                    "amount": str(row[1]),
                    "status": row[2],
                    "created_at": row[3].isoformat() if row[3] else None,
                }
                for row in rows
            ]
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail={"status": "degraded", "database": str(exc)}) from exc


@app.get("/api/customers")
def list_customers() -> dict[str, Any]:
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            rows = conn.execute(
                "SELECT customer_ref, name, created_at FROM customers ORDER BY created_at DESC LIMIT 10"
            ).fetchall()
        return {
            "items": [
                {
                    "customer_ref": row[0],
                    "name": row[1],
                    "created_at": row[2].isoformat() if row[2] else None,
                }
                for row in rows
            ]
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail={"status": "degraded", "database": str(exc)}) from exc
