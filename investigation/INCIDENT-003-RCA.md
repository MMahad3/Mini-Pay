# INCIDENT-003 RCA: Transaction Search Performance

## Symptoms

Transaction investigations become slower as volume grows. The support lookup filters on `transactions.transaction_ref`, but the baseline schema intentionally has no index for that column.

## Reproduction and data generation

The synthetic generator creates 1,000 customers, 50,000 transactions, duplicate references for investigation, and callback attempts:

```bash
python sql/generate_data.py > /tmp/minipay-seed.sql
wc -l /tmp/minipay-seed.sql
```

Load the schema and generated data into a disposable PostgreSQL database, then run:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, status, amount
FROM transactions
WHERE transaction_ref = 'TXN00012345';
```

The unindexed baseline uses a sequential scan as the table grows. Exact elapsed timings depend on PostgreSQL version, hardware, cache state, and whether the generated data is loaded locally, so this repository does not claim a portable millisecond result.

## Root cause

`transaction_ref` is a high-value support lookup field without a supporting index. PostgreSQL must inspect the table rather than navigating directly to matching rows. Duplicate references are intentionally present, so the index is non-unique.

## Corrective action

Apply the following migration after loading the baseline data:

```sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_transactions_ref
ON transactions(transaction_ref);
```

Repeat the same `EXPLAIN (ANALYZE, BUFFERS)` query. The expected plan changes from a sequential scan to an index-backed lookup with fewer heap/table buffers. The exact plan should be captured in the target environment before production rollout.

The recommendation and before/after query are also documented in [sql/PERFORMANCE.md](../sql/PERFORMANCE.md).

## Validation and preventive controls

- Generate at least 50,000 rows before comparing plans.
- Compare `EXPLAIN (ANALYZE, BUFFERS)` before and after the index.
- Check index size and write overhead before deployment.
- Add query-shape regression checks for support-critical lookups.
- Monitor query latency and sequential scans after release.
- Keep the index migration separate from seed data and run it through the normal database change process.
