import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psycopg
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://minipay:minipay@minipay-db.minipay.svc.cluster.local:5432/minipay",
)
BASE_DIR = Path(__file__).resolve().parent
API_KEY = os.getenv("MINIPAY_API_KEY", "dev-api-key")

app = FastAPI(title="MiniPay API")
customers: dict[int, dict[str, Any]] = {}
payments: dict[int, dict[str, Any]] = {}
customer_id_counter = 1
payment_id_counter = 1
idempotency_index: dict[str, int] = {}


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: str | None = None


class PaymentCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    idempotency_key: str | None = None


def ensure_auth(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def serialize_customer(customer_id: int, customer: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": customer_id,
        "name": customer["name"],
        "email": customer.get("email"),
        "created_at": customer["created_at"],
    }


def serialize_payment(payment_id: int, payment: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payment_id,
        "customer_id": payment["customer_id"],
        "amount": payment["amount"],
        "currency": payment["currency"],
        "status": payment["status"],
        "idempotency_key": payment.get("idempotency_key"),
        "created_at": payment["created_at"],
    }


@app.get("/")
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            conn.execute("SELECT 1")
        database_status = "ok"
    except Exception:
        database_status = "unavailable"

    return {"status": "ok", "database": database_status}


@app.get("/api/payments")
def list_payments() -> dict[str, Any]:
    return {"items": [serialize_payment(pid, payment) for pid, payment in sorted(payments.items())]}


@app.get("/api/customers")
def list_customers() -> dict[str, Any]:
    return {"items": [serialize_customer(cid, customer) for cid, customer in sorted(customers.items())]}


@app.post("/api/customers", status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> dict[str, Any]:
    ensure_auth(x_api_key)

    global customer_id_counter
    customer_id = customer_id_counter
    customer_id_counter += 1

    customer_record = {
        "name": payload.name,
        "email": payload.email,
        "created_at": utc_now(),
    }
    customers[customer_id] = customer_record
    return serialize_customer(customer_id, customer_record)


@app.post("/api/payments", status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> dict[str, Any]:
    ensure_auth(x_api_key)

    if payload.customer_id not in customers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found")

    if payload.idempotency_key and payload.idempotency_key in idempotency_index:
        payment_id = idempotency_index[payload.idempotency_key]
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"duplicate payment submission for idempotency_key '{payload.idempotency_key}'",
        )

    global payment_id_counter
    payment_id = payment_id_counter
    payment_id_counter += 1

    payment_record = {
        "customer_id": payload.customer_id,
        "amount": float(payload.amount),
        "currency": payload.currency.upper(),
        "status": "pending",
        "idempotency_key": payload.idempotency_key,
        "created_at": utc_now(),
    }
    payments[payment_id] = payment_record

    if payload.idempotency_key:
        idempotency_index[payload.idempotency_key] = payment_id

    return serialize_payment(payment_id, payment_record)


@app.get("/api/payments/{payment_id}")
def get_payment(payment_id: int, x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> dict[str, Any]:
    ensure_auth(x_api_key)

    payment = payments.get(payment_id)
    if payment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="payment not found")
    return serialize_payment(payment_id, payment)


@app.get("/api/customers/{customer_id}/payments")
def get_customer_payments(
    customer_id: int,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> dict[str, Any]:
    ensure_auth(x_api_key)

    if customer_id not in customers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found")

    customer_payments = [
        serialize_payment(payment_id, payment)
        for payment_id, payment in payments.items()
        if payment["customer_id"] == customer_id
    ]
    return {"customer_id": customer_id, "items": customer_payments}


@app.get("/api/_debug/error")
def simulated_server_error(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> dict[str, Any]:
    ensure_auth(x_api_key)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="simulated server error")
