-- 1. Transaction count and total value by status and day
SELECT
    created_at::date AS transaction_day,
    status,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_value
FROM transactions
GROUP BY created_at::date, status
ORDER BY transaction_day, status;

-- 2. Top 10 customers by successful transaction value
SELECT
    c.customer_ref,
    c.name,
    COUNT(t.id) AS successful_count,
    SUM(t.amount) AS successful_value
FROM customers c
JOIN transactions t ON t.customer_id = c.id
WHERE t.status = 'SUCCESS'
GROUP BY c.id, c.customer_ref, c.name
ORDER BY successful_value DESC
LIMIT 10;

-- 3. Transactions still PROCESSING after 15 minutes
SELECT
    id,
    transaction_ref,
    customer_id,
    amount,
    created_at
FROM transactions
WHERE status = 'PROCESSING'
  AND created_at < CURRENT_TIMESTAMP - INTERVAL '15 minutes'
ORDER BY created_at;

-- 4. Duplicate transaction references
SELECT
    transaction_ref,
    COUNT(*) AS occurrences,
    ARRAY_AGG(id ORDER BY id) AS transaction_ids
FROM transactions
GROUP BY transaction_ref
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;

-- 5. Daily success rate as percentage
SELECT
    created_at::date AS transaction_day,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'SUCCESS') / NULLIF(COUNT(*), 0),
        2
    ) AS success_rate_pct
FROM transactions
GROUP BY created_at::date
ORDER BY transaction_day;

-- 6. Reconciliation: successful transaction count/value vs callback-success count/value
SELECT
    COUNT(*) FILTER (WHERE t.status = 'SUCCESS') AS successful_transactions,
    COALESCE(SUM(t.amount) FILTER (WHERE t.status = 'SUCCESS'), 0) AS successful_value,
    COUNT(DISTINCT t.id) FILTER (
        WHERE t.status = 'SUCCESS' AND cb.callback_status = 'SUCCESS'
    ) AS callback_success_transactions,
    COALESCE(
        SUM(t.amount) FILTER (
            WHERE t.status = 'SUCCESS' AND cb.callback_status = 'SUCCESS'
        ),
        0
    ) AS callback_success_value
FROM transactions t
LEFT JOIN callbacks cb
  ON cb.transaction_id = t.id;

-- 7. Average and p95 processing time
SELECT
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) AS avg_processing_seconds,
    PERCENTILE_CONT(0.95) WITHIN GROUP (
        ORDER BY EXTRACT(EPOCH FROM (completed_at - created_at))
    ) AS p95_processing_seconds
FROM transactions
WHERE completed_at IS NOT NULL;
