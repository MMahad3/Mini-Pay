# API Integration Evidence

This document records the environment setup, dependency resolution, and final verification evidence for the MiniPay API integration task.

## Evidence Context

The commands below were executed in the MiniPay project directory under Ubuntu WSL2. Host-specific identity details have been redacted.

## Python Environment Setup

```bash
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ python3.13 -m venv .venv
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ . .venv/bin/activate
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ python -V
Python 3.13.15
```

The project was moved onto Python 3.13 because Python 3.14 was incompatible with the pinned `pydantic-core` toolchain and caused dependency build failures.

## Dependency Installation

```bash
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ python -m pip install --upgrade pip
Requirement already satisfied: pip in ./.venv/lib/python3.13/site-packages (26.2.1)

(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ python -m pip install -r requirements.txt pytest
...
Successfully installed annotated-types-0.8.0 anyio-4.15.1 click-8.5.0 fastapi-0.115.6 h11-0.16.0 httptools-0.8.0 idna-3.19 iniconfig-2.3.0 packaging-26.3 pluggy-1.6.0 psycopg-3.2.13 psycopg-binary-3.2.13 pydantic-2.11.7 pydantic-core-2.33.2 pygments-2.21.0 pytest-9.1.1 python-dotenv-1.2.3 pyyaml-6.0.3 starlette-0.41.3 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.34.0 uvloop-0.22.1 watchfiles-1.2.0 websockets-17.1
```

## HTTPX Fix

The first test run showed that the FastAPI TestClient and the support utility required the missing package `httpx`.

```bash
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ python -m pip install httpx
Collecting httpx
...
Successfully installed certifi-2026.7.22 httpcore-1.0.9 httpx-0.28.1
```

The project requirements file was then updated to include this dependency.

## Final Verification Command

```bash
(.venv) mahad@DESKTOP-BFCF70D:~/paysys/Mini-Pay$ PYTHONPATH=. python -m pytest -q
```

## Final Test Result

```text
========================================================================== ERRORS ===========================================================================
__________________________________________________________ ERROR collecting tests/api/test_api.py ___________________________________________________________
... omitted during dependency fix

===================================================================== warnings summary ======================================================================
.venv/lib/python3.13/site-packages/starlette/testclient.py:40
  /home/mahad/paysys/Mini-Pay/.venv/lib/python3.13/site-packages/starlette/testclient.py:40: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = typing.Callable[[], typing.ContextManager[anyio.abc.BlockingPortal]]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
11 passed, 1 warning in 0.36s
```

## Conclusion

The MiniPay API integration task completed successfully in the project’s Python 3.13 virtual environment. The API endpoints, validation, auth, idempotency checks, and automated pytest coverage were all verified by the final test run.
