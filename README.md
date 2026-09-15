# MiniPay Technical Assessment

MiniPay is a small FastAPI payment-processing demonstration with a browser UI, API automation, a Python support utility, PostgreSQL-oriented SQL investigations, and a Kubernetes deployment.

This repository is the my submission for the Paysys Labs DevOps / Implementation and L2 Support assessment. It is designed to be reproducible by an evaluator and contains implementation, tests, operational evidence, and incident findings.

## Quick Start

Requirements: Python 3.12 or 3.13, `pip`, and Chromium managed by Playwright for GUI tests.

```bash
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
PYTHONPATH=. python -m pytest -q tests/unit tests/api
PYTHONPATH=. python -m pytest -q tests/gui/test_gui.py
```

The GUI fixture starts Uvicorn automatically. To run the application manually:

```bash
MINIPAY_API_KEY=dev-api-key PYTHONPATH=. python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` and use the development key `dev-api-key` only for local evaluation.

For the complete setup, Docker/Minikube deployment, environment variables, and troubleshooting commands, see [SETUP.md](SETUP.md).

## Repository Guide

| Area | Contents |
| --- | --- |
| `app/` | FastAPI service and static browser UI |
| `python/` | Transaction diagnosis and health/support CLI |
| `sql/` | Investigation queries and indexing recommendation |
| `kubernetes/` | Namespace, PostgreSQL StatefulSet, API Deployment, Services, and probes |
| `tests/api/` | FastAPI endpoint and error-path tests |
| `tests/unit/` | Support utility unit tests |
| `tests/gui/` | Playwright browser journeys |
| `tests/ui/` | Assessment-required UI test entry point and run instructions |
| `investigation/` | Kubernetes troubleshooting findings and corrective actions |
| `evidence/` | Reproducible test and operational evidence |
| `Picture-Proofs/` | UI and Rancher screenshots |

See [ARCHITECTURE.md](ARCHITECTURE.md) for component boundaries and [AI_USAGE.md](AI_USAGE.md) for AI-assisted work and validation.

## Assessment Coverage

| Assessment area | Status | Evidence |
| --- | --- | --- |
| Linux and troubleshooting | Complete | [evidence/linux.md](evidence/linux.md) |
| Git workflow | Repository history and final tag required | Run `git log --oneline` and create `submission-v1.0` before publishing |
| SQL | Complete | [sql/queries.sql](sql/queries.sql), [sql/PERFORMANCE.md](sql/PERFORMANCE.md) |
| Kubernetes | Complete for Minikube validation | [kubernetes/minipay.yaml](kubernetes/minipay.yaml), [evidence/kubernetes.md](evidence/kubernetes.md) |
| Rancher | Attempt and blocker documented | [evidence/rancher.md](evidence/rancher.md) |
| Python support utility | Complete | [python/support_tool.py](python/support_tool.py), [tests/unit/test_support_tool.py](tests/unit/test_support_tool.py) |
| API automation | Complete | [tests/api/test_api.py](tests/api/test_api.py), [evidence/API-Integration.md](evidence/API-Integration.md) |
| GUI automation | Complete for Chromium smoke journeys | [tests/gui/test_gui.py](tests/gui/test_gui.py), [evidence/gui-test-run.md](evidence/gui-test-run.md) |
| L2 investigation | Complete with documented limitations | [investigation/](investigation/), [evidence/](evidence/) |

## Known Limitations

- Customer and payment API data is held in process memory. PostgreSQL is currently used by `/health` and is the target database for the SQL/support-tool investigation workflow; the demo CRUD endpoints do not persist to it.
- The default API key and local database values are development-only examples. Production deployments must inject credentials through a secret manager or Kubernetes Secrets and must set `MINIPAY_API_KEY` explicitly.
- Rancher was started locally with Docker, but a full Rancher-managed cluster workflow was not completed; the constraint and commands are documented in [evidence/rancher.md](evidence/rancher.md).
- Evidence records the original WSL environment for traceability. It contains no real credentials or private keys.

