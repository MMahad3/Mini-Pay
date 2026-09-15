# Architecture

## Scope

MiniPay is a deliberately small assessment application. It demonstrates a web UI, authenticated REST endpoints, operational health checks, a support utility, SQL investigation, and a Kubernetes deployment.

## Components

```text
Browser
  |
  v
FastAPI + static UI (Uvicorn :8000 locally, :8080 in container)
  |-- /health -> PostgreSQL connectivity check
  |-- /api/customers and /api/payments -> in-process demo state
  |
  +--> PostgreSQL (Kubernetes StatefulSet :5432)
         |-- schema/init data for SQL and support-tool investigations
         +-- persistent volume claim
```

## Application

- `app/main.py` defines the FastAPI routes, Pydantic request validation, API-key check, idempotency guard, and health endpoint.
- `app/static/index.html` is a dependency-free browser UI using stable `data-testid` attributes for Playwright.
- The API key is read from `MINIPAY_API_KEY`; the local fallback is only for development and tests.
- `/health` returns service health and reports PostgreSQL availability without making the API unusable when the dependency is down.

## Data and supportability

The API demo state is currently stored in Python dictionaries, which keeps the assessment self-contained and fast but is not durable or safe for multiple replicas. PostgreSQL is initialized with customers, transactions, and callbacks tables for the SQL/support-tool tasks and is checked by the health endpoint. A production implementation would move API reads/writes to PostgreSQL, add migrations, enforce database-level idempotency, and use connection pooling.

The support utility attempts an API transaction lookup first and falls back to PostgreSQL when the API is unavailable. It provides bounded HTTP/database timeouts, JSON output, health reporting, and stuck-transaction summaries.

## Kubernetes

`kubernetes/minipay.yaml` creates:

- `minipay` namespace
- PostgreSQL Secret, ConfigMap, StatefulSet, headless Service, readiness/liveness probes, and PVC
- Two API replicas with resource requests/limits and HTTP readiness/liveness probes
- NodePort Service routing port 80 to API container port 8080

The local Minikube image uses `imagePullPolicy: Never`. A production cluster should use an immutable registry image and an external secret manager.

## Validation boundaries

- Unit tests cover support diagnosis rules.
- API tests cover authentication, validation, CRUD responses, idempotency, 404s, simulated 500s, and health latency.
- GUI tests cover login, customer creation, payment submission/search, and a negative payment path.
- Kubernetes evidence covers image build, rollout, pod readiness, service access, and health checks.
- Rancher evidence documents the Docker permission and privileged-container blocker/resolution.
