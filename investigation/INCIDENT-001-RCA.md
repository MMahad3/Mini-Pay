# INCIDENT-001 RCA: Intermittent Transaction Search Failure

## Status

The reported intermittent HTTP 500 was not reproduced in the submitted implementation. The current payment lookup returns a controlled 404 for an unknown payment and validates the API key before lookup. The repository does not have a production database-backed search path, so claiming a confirmed database root cause would be inaccurate.

## Observations and reproduction

Reproduce the supported lookup paths with the API running:

```bash
curl -i -H 'X-API-Key: dev-api-key' http://127.0.0.1:8000/api/payments/99999
curl -i -H 'X-API-Key: dev-api-key' http://127.0.0.1:8000/api/_debug/error
```

The first request returns `404 payment not found`. The second is a deliberate controlled `500 simulated server error` used to verify error-path automation. Repeated valid lookups and unknown IDs did not produce intermittent 500 responses; the API test suite covers both outcomes.

## Hypotheses considered

- Incorrect or missing authentication header: rejected as a likely cause of 500; the expected response is 401.
- Unknown payment identifier: rejected; the implementation returns 404.
- Application exception during a database query: not applicable to the current in-memory lookup implementation, but this is the most likely production cause for a real database-backed service.
- Inconsistent replicas: possible in the current design because state is process-local; different API replicas would not share customer/payment state. This is a real design risk, although it was not observable in the single-process test fixture.

## Root cause assessment

No confirmed root cause for the original incident. The principal architectural risk identified is non-persistent, process-local payment state. In a multi-replica deployment, a request routed to a different replica may not find data created by the first replica. If that path were implemented with an unhandled lookup or database exception, it could surface as intermittent 500 responses.

## Immediate corrective action

- Added API tests for unknown resources, authentication, successful lookup, and deliberate server error behavior.
- Added Kubernetes readiness/liveness checks and documented rollout/log inspection procedures.
- Recorded the limitation rather than presenting a non-reproducible hypothesis as a verified fix.

## Permanent corrective and preventive action

- Persist customer/payment records in PostgreSQL and enforce database-level constraints.
- Use a shared database or cache for all API replicas; do not rely on process-local dictionaries.
- Add structured request/error logging with correlation IDs.
- Map database not-found and transient failures to explicit 404/5xx responses.
- Add a multi-replica integration test that creates a payment and retrieves it through another replica.
- Alert on elevated 5xx rates and examine pod-specific logs and endpoints.

## Validation

```text
PYTHONPATH=. python -m pytest -q tests/api
9 passed
```

The result validates the implemented behavior and the controlled 500 path. It does not claim that the original intermittent production fault was reproduced.
