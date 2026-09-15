# Setup and Reproduction

## Local Python workflow

Use Python 3.12 or 3.13. Python 3.13 was used for the recorded test evidence.

```bash
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Run the non-browser tests:

```bash
PYTHONPATH=. python -m pytest -q tests/unit tests/api
```

Run the browser tests. The fixture starts and stops a local Uvicorn process automatically:

```bash
PYTHONPATH=. python -m pytest -q tests/gui/test_gui.py --maxfail=1
```

Run all tests:

```bash
PYTHONPATH=. python -m pytest -q
```

## Run the API manually

```bash
export MINIPAY_API_KEY=dev-api-key
export DATABASE_URL=postgresql://minipay:minipay@127.0.0.1:5432/minipay
PYTHONPATH=. python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The health endpoint does not fail the process when PostgreSQL is unavailable; it reports `database: unavailable`. API mutations require the `X-API-Key` header. The local UI can be opened at `http://127.0.0.1:8000`.

## Docker

Build and run the API container:

```bash
docker build -t minipay-api:local .
docker run --rm -p 8080:8080 \
  -e MINIPAY_API_KEY=dev-api-key \
  -e DATABASE_URL=postgresql://minipay:minipay@host.docker.internal:5432/minipay \
  minipay-api:local
```

Check it with:

```bash
./scripts/healthcheck.sh http://127.0.0.1:8080/health
```

## Minikube deployment

The manifest uses a local image, so build it in the Minikube image environment or with `minikube image build`:

```bash
minikube start
minikube image build -t minipay-api:local .
kubectl apply -f kubernetes/minipay.yaml
kubectl -n minipay rollout status statefulset/minipay-db --timeout=180s
kubectl -n minipay rollout status deployment/minipay-api --timeout=180s
kubectl -n minipay get pods,svc
```

Expose the API locally:

```bash
kubectl -n minipay port-forward svc/minipay-api 8080:80
```

In another terminal:

```bash
./scripts/healthcheck.sh http://127.0.0.1:8080/health
```

The committed manifest contains only development fixture values. For a real environment, replace them through an external secret workflow, set `imagePullPolicy` appropriately, use a registry image, and review storage, network policy, TLS, and backup settings.

## Support utility

The utility reads `MINIPAY_API_URL`, `MINIPAY_API_KEY`, and `MINIPAY_DB_URL`. It supports an API-first transaction lookup with database fallback, health checks, and stuck-transaction summaries:

```bash
MINIPAY_API_URL=http://127.0.0.1:8000 \
MINIPAY_API_KEY=dev-api-key \
PYTHONPATH=. python -m python.support_tool --health-check
PYTHONPATH=. python -m python.support_tool --transaction TXN000123 --json
PYTHONPATH=. python -m python.support_tool --stuck
```

The transaction and stuck-transaction commands require the assessment database schema from `kubernetes/minipay.yaml` to be populated.

## Reproducibility notes

- No committed virtual environment, browser binary, database volume, or generated test cache is required.
- No real password, token, private key, or employer/client data belongs in this repository.
- See `evidence/` for the recorded validation output and `investigation/` for operational findings.
