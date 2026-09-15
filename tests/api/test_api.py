import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_customer_success():
    response = client.post(
        "/api/customers",
        json={"name": "Alice Johnson", "email": "alice@example.com"},
        headers={"X-API-Key": "dev-api-key"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "Alice Johnson"
    assert payload["email"] == "alice@example.com"
    assert "id" in payload
    assert "created_at" in payload


def test_create_payment_success_and_schema():
    customer = client.post(
        "/api/customers",
        json={"name": "Bob Smith", "email": "bob@example.com"},
        headers={"X-API-Key": "dev-api-key"},
    ).json()

    response = client.post(
        "/api/payments",
        json={
            "customer_id": customer["id"],
            "amount": 125.5,
            "currency": "USD",
            "idempotency_key": "pay-001",
        },
        headers={"X-API-Key": "dev-api-key"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["customer_id"] == customer["id"]
    assert payload["amount"] == 125.5
    assert payload["currency"] == "USD"
    assert payload["status"] == "pending"
    assert "id" in payload
    assert "created_at" in payload


def test_missing_or_invalid_fields_are_rejected():
    bad_customer = client.post(
        "/api/customers",
        json={"email": "missing-name@example.com"},
        headers={"X-API-Key": "dev-api-key"},
    )
    assert bad_customer.status_code == 422

    bad_payment = client.post(
        "/api/payments",
        json={"customer_id": 999, "currency": "USD"},
        headers={"X-API-Key": "dev-api-key"},
    )
    assert bad_payment.status_code == 422


def test_unknown_customer_and_payment_resources():
    missing_customer = client.get(
        "/api/customers/999/payments",
        headers={"X-API-Key": "dev-api-key"},
    )
    assert missing_customer.status_code == 404

    missing_payment = client.get(
        "/api/payments/99999",
        headers={"X-API-Key": "dev-api-key"},
    )
    assert missing_payment.status_code == 404


def test_unauthorized_access_requires_api_key():
    response = client.get("/api/customers/1/payments")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_duplicate_idempotency_key_is_rejected():
    customer = client.post(
        "/api/customers",
        json={"name": "Carol White", "email": "carol@example.com"},
        headers={"X-API-Key": "dev-api-key"},
    ).json()

    first = client.post(
        "/api/payments",
        json={
            "customer_id": customer["id"],
            "amount": 42.0,
            "currency": "USD",
            "idempotency_key": "idempotent-dup",
        },
        headers={"X-API-Key": "dev-api-key"},
    )
    assert first.status_code == 201

    duplicate = client.post(
        "/api/payments",
        json={
            "customer_id": customer["id"],
            "amount": 42.0,
            "currency": "USD",
            "idempotency_key": "idempotent-dup",
        },
        headers={"X-API-Key": "dev-api-key"},
    )
    assert duplicate.status_code == 409
    assert "duplicate" in duplicate.json()["detail"].lower()


def test_server_error_response_is_returned_for_simulated_failure():
    response = client.get("/api/_debug/error", headers={"X-API-Key": "dev-api-key"})
    assert response.status_code == 500
    assert response.json()["detail"] == "simulated server error"


def test_response_time_is_within_reasonable_threshold():
    start = time.perf_counter()
    response = client.get("/health")
    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 0.5
