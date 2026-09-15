# GUI Test Run Evidence

## Command

Executed from Ubuntu WSL2 in the project virtual environment:

```bash
cd /home/mahad/paysys/Mini-Pay
. .venv/bin/activate
PYTHONPATH=. python -m pytest tests/gui/test_gui.py -q --maxfail=1
```

## Result

```text
..                                                                       [100%]
2 passed in 1.91s
```

## Covered journeys

- Login to the dashboard with the development API key.
- Create a customer and submit a payment.
- Search for the submitted payment and verify `status=pending`.
- Submit a payment for customer `999` and verify the `customer not found` error.