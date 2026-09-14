# Python Unit Test Evidence

## Support Utility

The Mini-Pay Python CLI support utility is implemented in [`python/support_tool.py`](../python/support_tool.py). It provides transaction diagnosis, API and database fallback lookups, health checks, and stuck-transaction summaries.

## Unit Tests

The core diagnosis logic is covered by [`tests/unit/test_support_tool.py`](../tests/unit/test_support_tool.py). The tests verify that:

- Processing transactions are flagged as anomalous.
- Failed transactions include a recommended next action.

## Test Environment

The test environment was created in a Python virtual environment to satisfy Ubuntu’s externally managed Python installation restrictions.

## Test Command

```bash
python -m pytest -q tests/unit
```

## Test Result

```text
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ python -m pytest -q tests/unit
..                                      [100%]
2 passed in 0.09s
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$
```

All two unit tests passed successfully.