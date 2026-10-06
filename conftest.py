"""pytest fixtures + HTML report.

`api`             — one ShopApi client for the whole run.
`user`            — fresh Faker data, nothing created on the server.
`registered_user` — account created before the test, deleted after it.
"""

import logging
import os
import subprocess
from pathlib import Path

import pytest
from dotenv import load_dotenv

from api.shop_api import ShopApi
from data.user import User, build_user

load_dotenv(Path(__file__).resolve().parent / ".env")
DEFAULT_BASE_URL = "https://automationexercise.com/api"

log = logging.getLogger("tests")


def pytest_runtest_logstart(nodeid, location):
    """Mark where each test starts in logs/test_run.log."""
    log.info("===== START %s", nodeid)


def pytest_runtest_logreport(report):
    if report.when == "call" or report.outcome != "passed":
        log.info("===== %s %s (%s)", report.outcome.upper(), report.nodeid, report.when)


def pytest_sessionfinish(session, exitstatus):
    """Build a single-file HTML report (opens straight from disk, no server)."""
    root = Path(session.config.rootpath)
    results = root / "allure-results"
    report = root / "reports"
    if not results.exists():
        return
    try:
        subprocess.run(
            [
                "allure",
                "generate",
                str(results),
                "-o",
                str(report),
                "--clean",
                "--single-file",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("\nAllure CLI missing — install it to get reports/index.html")
        return
    except subprocess.CalledProcessError as exc:
        print(f"\nAllure generate failed:\n{exc.stderr}")
        return
    print(f"\nAllure HTML: {report / 'index.html'}")


@pytest.fixture(scope="session")
def api() -> ShopApi:
    return ShopApi(os.getenv("BASE_URL", DEFAULT_BASE_URL))


@pytest.fixture
def user() -> User:
    return build_user()


@pytest.fixture
def registered_user(api: ShopApi, user: User):
    """Create the account, hand it to the test, always delete it afterwards."""
    body = api.create_account(user).json()
    assert body["responseCode"] == 201, body
    yield user
    # Teardown must not fail the test: the test may have deleted it already.
    api.delete_account(user.email, user.password)
