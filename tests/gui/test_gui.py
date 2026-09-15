import os
import re
import subprocess
import sys
import time
import urllib.request

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _wait_for_server(url: str, timeout: int = 30) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError(f"Timed out waiting for app at {url}")


@pytest.fixture(scope="session", autouse=True)
def app_server():
    env = os.environ.copy()
    env["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + env.get("PYTHONPATH", "")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=PROJECT_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        _wait_for_server("http://127.0.0.1:8000/health")
        yield
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)


def _launch_page() -> tuple[object, Browser, BrowserContext, Page]:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    return playwright, browser, context, page


def test_login_and_customer_payment_flow():
    playwright, browser, context, page = _launch_page()
    try:
        page.goto("http://127.0.0.1:8000")

        page.get_by_test_id("api-key-input").fill("dev-api-key")
        page.get_by_test_id("login-button").click()

        assert "Logged in" in page.get_by_test_id("customer-result").text_content()

        page.get_by_test_id("customer-name").fill("Playwright User")
        page.get_by_test_id("customer-email").fill("playwright@example.com")
        page.get_by_test_id("customer-submit").click()

        customer_result = page.get_by_test_id("customer-result")
        assert "Customer created" in customer_result.text_content()

        page.get_by_test_id("payment-customer-id").fill("1")
        page.get_by_test_id("payment-amount").fill("89.99")
        page.get_by_test_id("payment-idempotency").fill("ui-payment-001")
        page.get_by_test_id("payment-submit").click()

        payment_result = page.get_by_test_id("payment-result")
        assert "Payment submitted" in payment_result.text_content()

        payment_id_match = re.search(r"#(\d+)", payment_result.text_content())
        assert payment_id_match is not None
        payment_id = payment_id_match.group(1)

        page.get_by_test_id("search-id").fill(payment_id)
        page.get_by_test_id("search-button").click()

        search_result = page.get_by_test_id("search-result")
        assert "status=pending" in search_result.text_content()
    finally:
        context.close()
        browser.close()
        playwright.stop()


def test_negative_error_path_for_bad_payment():
    playwright, browser, context, page = _launch_page()
    try:
        page.goto("http://127.0.0.1:8000")
        page.get_by_test_id("api-key-input").fill("dev-api-key")
        page.get_by_test_id("login-button").click()

        page.get_by_test_id("payment-customer-id").fill("999")
        page.get_by_test_id("payment-amount").fill("10")
        page.get_by_test_id("payment-submit").click()

        error_result = page.get_by_test_id("payment-result")
        assert "customer not found" in error_result.text_content()
    finally:
        context.close()
        browser.close()
        playwright.stop()
