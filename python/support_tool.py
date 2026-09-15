#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
from typing import Any

import httpx
import psycopg

LOGGER = logging.getLogger("support_tool")


def load_config() -> dict[str, str]:
    return {
        "api_url": os.getenv("MINIPAY_API_URL", "http://127.0.0.1:8080"),
        "api_key": os.getenv("MINIPAY_API_KEY", "dev-api-key"),
        "db_url": os.getenv(
            "MINIPAY_DB_URL",
            "postgresql://minipay:minipay@127.0.0.1:5432/minipay",
        ),
    }


def diagnose_transaction(txn: dict[str, Any]) -> dict[str, Any]:
    anomalies: list[str] = []
    recommended_next_action = "No anomaly detected; continue normal monitoring."

    status = str(txn.get("status") or "").upper()
    failure_code = txn.get("failure_code")
    last_callback_status = txn.get("last_callback_status")
    callback_attempts = int(txn.get("callback_attempts") or 0)

    if status == "PROCESSING":
        anomalies.append("transaction is still processing beyond expected time")
        recommended_next_action = "Check upstream worker status and retry queue; confirm if payment is stuck in processing."

    if failure_code:
        anomalies.append(f"failure code detected: {failure_code}")
        recommended_next_action = "Review upstream failure reason and retry if safe."

    if last_callback_status and last_callback_status.upper() != "SUCCESS":
        anomalies.append("latest callback did not succeed")
        recommended_next_action = "Check callback job and retry callback delivery or investigate downstream service."

    if status == "FAILED":
        anomalies.append("transaction final status is FAILED")
        recommended_next_action = "Review failure reason, reconcile ledger state, and retry only if idempotent."

    if status == "SUCCESS" and callback_attempts and last_callback_status and last_callback_status.upper() != "SUCCESS":
        anomalies.append("payment succeeded but callback reconciliation is incomplete")
        recommended_next_action = "Investigate reconciliation gap and replay callback if required."

    return {
        "transaction_ref": txn.get("transaction_ref"),
        "status": status,
        "customer_ref": txn.get("customer_ref"),
        "customer_name": txn.get("customer_name"),
        "amount": txn.get("amount"),
        "created_at": txn.get("created_at"),
        "completed_at": txn.get("completed_at"),
        "failure_code": failure_code,
        "callback_attempts": callback_attempts,
        "last_callback_status": last_callback_status,
        "anomalies": anomalies,
        "recommended_next_action": recommended_next_action,
    }


def fetch_from_api(transaction_ref: str, cfg: dict[str, str]) -> dict[str, Any]:
    url = f"{cfg['api_url'].rstrip('/')}/api/payments/{transaction_ref}"
    headers = {"X-API-Key": cfg["api_key"]}
    response = httpx.get(url, headers=headers, timeout=5.0)
    if response.status_code == 404:
        raise LookupError(f"transaction not found: {transaction_ref}")
    response.raise_for_status()
    return response.json()


def fetch_from_db(transaction_ref: str, cfg: dict[str, str]) -> dict[str, Any]:
    with psycopg.connect(cfg["db_url"], connect_timeout=5) as conn:
        row = conn.execute(
            """
            SELECT
                t.transaction_ref,
                c.customer_ref,
                c.name,
                t.amount,
                t.status,
                t.created_at,
                t.completed_at,
                t.failure_code,
                COUNT(cb.id) AS callback_attempts,
                (
                    SELECT cb2.callback_status
                    FROM callbacks cb2
                    WHERE cb2.transaction_id = t.id
                    ORDER BY cb2.attempt_no DESC
                    LIMIT 1
                ) AS last_callback_status
            FROM transactions t
            JOIN customers c ON c.id = t.customer_id
            LEFT JOIN callbacks cb ON cb.transaction_id = t.id
            WHERE t.transaction_ref = %s
            GROUP BY
                t.transaction_ref, c.customer_ref, c.name, t.amount,
                t.status, t.created_at, t.completed_at, t.failure_code, t.id
            LIMIT 1
            """,
            (transaction_ref,),
        ).fetchone()

    if not row:
        raise LookupError(f"transaction not found: {transaction_ref}")

    return {
        "transaction_ref": row[0],
        "customer_ref": row[1],
        "customer_name": row[2],
        "amount": str(row[3]),
        "status": row[4],
        "created_at": row[5].isoformat() if row[5] else None,
        "completed_at": row[6].isoformat() if row[6] else None,
        "failure_code": row[7],
        "callback_attempts": row[8],
        "last_callback_status": row[9],
    }


def fetch_transaction(transaction_ref: str, cfg: dict[str, str]) -> dict[str, Any]:
    try:
        return fetch_from_api(transaction_ref, cfg)
    except (httpx.HTTPError, httpx.TimeoutException, LookupError):
        LOGGER.warning("API lookup failed for %s, falling back to DB", transaction_ref)
    try:
        return fetch_from_db(transaction_ref, cfg)
    except Exception as exc:
        raise RuntimeError(f"unable to retrieve transaction {transaction_ref}: {exc}") from exc


def summarize_stuck_transactions(cfg: dict[str, str]) -> dict[str, Any]:
    with psycopg.connect(cfg["db_url"], connect_timeout=5) as conn:
        rows = conn.execute(
            """
            SELECT transaction_ref, amount, status, created_at, failure_code
            FROM transactions
            WHERE status IN ('PROCESSING', 'FAILED')
              OR created_at < NOW() - INTERVAL '15 minutes'
            ORDER BY created_at DESC
            LIMIT 20
            """
        ).fetchall()

    return {
        "count": len(rows),
        "items": [
            {
                "transaction_ref": row[0],
                "amount": str(row[1]),
                "status": row[2],
                "created_at": row[3].isoformat() if row[3] else None,
                "failure_code": row[4],
            }
            for row in rows
        ],
    }


def health_check(cfg: dict[str, str]) -> dict[str, Any]:
    status = {"api": "unknown", "database": "unknown"}
    try:
        response = httpx.get(f"{cfg['api_url'].rstrip('/')}/health", timeout=5.0)
        status["api"] = "ok" if response.status_code == 200 else "degraded"
    except Exception:
        status["api"] = "down"

    try:
        with psycopg.connect(cfg["db_url"], connect_timeout=5) as conn:
            conn.execute("SELECT 1")
        status["database"] = "ok"
    except Exception:
        status["database"] = "down"

    overall = "ok" if status["api"] == "ok" and status["database"] == "ok" else "degraded"
    return {"status": overall, "checks": status}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MiniPay transaction support utility")
    parser.add_argument("--transaction", required=False, help="Transaction reference")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--health-check", action="store_true", help="Check API and DB health")
    parser.add_argument("--stuck", action="store_true", help="List potentially stuck or failed transactions")
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    cfg = load_config()

    try:
        if args.health_check:
            report = health_check(cfg)
            print(json.dumps(report, indent=2))
            return 0 if report["status"] == "ok" else 1

        if args.stuck:
            report = summarize_stuck_transactions(cfg)
            print(json.dumps(report, indent=2))
            return 0 if report["count"] >= 0 else 1

        if not args.transaction:
            parser.error("you must provide --transaction, --health-check, or --stuck")

        txn = fetch_transaction(args.transaction, cfg)
        report = diagnose_transaction(txn)

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"Transaction: {report['transaction_ref']}")
            print(f"Customer: {report['customer_ref']} / {report['customer_name']}")
            print(f"Amount: {report['amount']}")
            print(f"Status: {report['status']}")
            print(f"Created: {report['created_at']}")
            print(f"Completed: {report['completed_at']}")
            print(f"Callback attempts: {report['callback_attempts']}")
            print(f"Last callback status: {report['last_callback_status']}")
            print(f"Anomalies: {report['anomalies'] or 'none'}")
            print(f"Next action: {report['recommended_next_action']}")

        return 0

    except LookupError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except (httpx.HTTPError, httpx.TimeoutException, psycopg.Error, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 4
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
