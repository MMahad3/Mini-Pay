# GUI Test Automation

These browser tests exercise the MiniPay UI using Playwright.

## Requirements

- Python 3.13+
- Project virtual environment activated
- Playwright browser binaries installed

## Install

```bash
cd /home/mahad/paysys/Mini-Pay
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

## Run

The test suite starts the MiniPay app automatically before each session, so a single command is sufficient:

```bash
cd /home/mahad/paysys/Mini-Pay
. .venv/bin/activate
PYTHONPATH=. python -m pytest tests/gui/test_gui.py -q --maxfail=1
```

## What these tests cover

1. Open/login to the dashboard
2. Create a customer
3. Submit a payment
4. Search for the payment by ID
5. Validate a negative scenario for a missing customer

The selectors are stable `data-testid` attributes, and the test fixture starts and stops the local Uvicorn server automatically. The browser tests currently exercise the dashboard's client-side workflow; API-level behavior is covered separately by `tests/api/test_api.py`.

## Latest evidence

The latest completed run is documented in [evidence/gui-test-run.md](../../evidence/gui-test-run.md).

## CI suggestion

- Run the GUI smoke tests on every pull request and release branch.
- Keep this suite small and fast for the main pipeline.
- Run a larger cross-browser and validation regression suite nightly or before release.
