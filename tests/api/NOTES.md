# API integration notes

For payment integrations, client and server timeouts should be handled explicitly. The client should use a bounded timeout for each HTTP call, fail fast on timeouts, and retry only for transient network or 5xx responses. Server-side endpoints should also enforce a short request timeout so that hung downstream calls do not block the service indefinitely.

Retries should be limited and safe. For payment systems, retries are only appropriate for idempotent operations or when the request can be safely deduplicated with an idempotency key. A duplicate payment should not create a second charge, so the API should store the idempotency key and return the original result instead of processing the same payment again.

4xx errors should be treated as client-side or validation problems and retried only with a fix to the request. 5xx errors are server-side faults and are often retriable when the operation is safe to repeat, but an alert should be raised and the failure recorded for operations support. In practice, payment endpoints should distinguish validation issues, auth failures, not-found conditions, and duplicate submissions from upstream dependency failures so that operators can react appropriately.
