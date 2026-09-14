from python.support_tool import diagnose_transaction

def test_processing_transaction_is_flagged():
    payload = {
        "transaction_ref": "TXN000123",
        "customer_ref": "CUST000001",
        "customer_name": "Test Customer",
        "amount": "25.00",
        "status": "PROCESSING",
        "created_at": "2026-09-14T12:00:00",
        "completed_at": None,
        "failure_code": None,
        "callback_attempts": 0,
        "last_callback_status": None,
    }

    result = diagnose_transaction(payload)
    assert "transaction is still processing beyond expected time" in result["anomalies"]
    assert "Next action" not in result  # this is only a sanity check, not required


def test_failed_transaction_has_recommended_action():
    payload = {
        "transaction_ref": "TXN000456",
        "customer_ref": "CUST000002",
        "customer_name": "Another Customer",
        "amount": "100.00",
        "status": "FAILED",
        "created_at": "2026-09-14T12:10:00",
        "completed_at": "2026-09-14T12:12:00",
        "failure_code": "UPSTREAM_ERROR",
        "callback_attempts": 2,
        "last_callback_status": "FAILED",
    }

    result = diagnose_transaction(payload)
    assert "FAILED" in result["status"]
    assert "failure code detected" in result["anomalies"][0]
    assert "recommended_next_action" in result
