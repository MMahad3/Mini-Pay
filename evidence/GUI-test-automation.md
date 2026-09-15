# GUI Test Automation Evidence

## Application UI

The MiniPay browser UI is served by the FastAPI application at `http://localhost:8000`. The UI provides controls for dashboard login, customer creation, payment submission, and payment search.

The screenshot in /Picture-Proofs/'Minipay Gui.png' is the visual proof of the MiniPay application UI.
## Automation Framework

The GUI tests use Playwright with Chromium. The test implementation is available in [`tests/gui/test_gui.py`](../tests/gui/test_gui.py), and the run instructions are documented in [`tests/gui/README.md`](../tests/gui/README.md).

The tests use stable `data-testid` selectors rather than fragile timing-only logic. The test fixture starts the local Uvicorn server automatically and stops the browser and server after the test session.

## Automated Journeys

The test suite validates:

1. Open the application and log in with the development API key.
2. Create a customer.
3. Submit a test payment.
4. Search for the submitted payment by its returned ID.
5. Validate the successful payment result and `pending` status.
6. Submit a payment for a missing customer and validate the `customer not found` error.

## Test Environment

The tests were executed in Ubuntu WSL2 from the project Python virtual environment.

## Test Command

```bash
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ PYTHONPATH=. python -m pytest tests/gui/test_gui.py -q --maxfail=1
```

## Test Result

```text
..                                                                       [100%]
2 passed in 1.92s
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$
```

Both GUI automation tests passed successfully. The result covers the successful payment/search journey and the negative missing-customer scenario.

## CI and Release Plan

Run the GUI smoke tests on every pull request and release branch together with the unit and API tests. Publish the test output as a CI artifact and fail the pipeline when a GUI test fails.

Run a larger regression suite nightly and before production releases. The regression suite should include additional browser and viewport combinations, validation boundaries, repeated submissions, and API/UI consistency checks.
