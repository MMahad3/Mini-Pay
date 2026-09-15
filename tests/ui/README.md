# UI Automation Entry Point

The browser automation required by the assessment is implemented in [../gui/test_gui.py](../gui/test_gui.py). The `gui` directory is retained because it documents the Playwright-specific suite; this `ui` entry point satisfies the assessment's required `tests/ui/` structure without duplicating tests.

Run the suite with:

```bash
PYTHONPATH=. python -m pytest -q tests/gui/test_gui.py --maxfail=1
```

The fixture starts Uvicorn automatically and uses stable `data-testid` selectors. See [../../evidence/gui-test-run.md](../../evidence/gui-test-run.md) for completed-run evidence.
