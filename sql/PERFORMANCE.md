# SQL Performance Investigation

## Problem
The schema intentionally has minimal indexing. Transaction support workflows often search by `transaction_ref`, and without an index this creates a full table scan as the dataset grows.

## Slow query (before)
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, status, amount
FROM transactions
WHERE transaction_ref = 'TXN00012345';
```

This query is inefficient because PostgreSQL must read many rows to find the matching reference. On a dataset of 50,000+ transactions, the cost grows as the table grows.

## Root cause
`transactions.transaction_ref` is not indexed. The table has no supporting index for point lookup or support queries.

## Improvement
Add an index on the lookup column:

```sql
CREATE INDEX idx_transactions_ref
ON transactions(transaction_ref);
```

This makes the lookup efficient and reduces table scans.

## Fast query (after)
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, status, amount
FROM transactions
WHERE transaction_ref = 'TXN00012345';
```

After the index is added, PostgreSQL should use an index scan instead of a sequential scan, reducing buffer reads and execution time.

## Why this matters
This is a realistic production issue: support engineers often search by transaction reference during investigations. Without the index, latency increases as the table grows, and searches become slow.

## Recommendation
Keep the index in production and validate future query patterns with `EXPLAIN (ANALYZE, BUFFERS)` before rollout. Add additional indexes only where the workload justifies them.
