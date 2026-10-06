"""Thin wrapper around requests.Session.

One place for: base URL, timeout, retries, logging, Allure attachments.
Endpoint methods live in `shop_api.py`, not here.
"""

import json
import logging

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger(__name__)

# Never write these values to logs or the report.
SECRET_FIELDS = {"password"}


def _mask(data: dict | None) -> dict | None:
    if not data:
        return data
    return {k: ("***" if k in SECRET_FIELDS else v) for k, v in data.items()}


class BaseClient:
    def __init__(self, base_url: str, timeout: float = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        # The public demo site is slow and sometimes drops connections.
        # Retry network errors and 5xx only — never hide a real 4xx.
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=(502, 503, 504),
            allowed_methods=None,  # retry POST/PUT/DELETE too
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        sent = _mask(kwargs.get("data") or kwargs.get("params"))
        log.info("%s %s %s", method, url, sent or "")

        response = self.session.request(method, url, timeout=self.timeout, **kwargs)

        log.info("-> HTTP %s %s", response.status_code, response.text[:300])
        allure.attach(
            f"{method} {url}\n{json.dumps(sent, indent=2) if sent else ''}",
            name=f"request {method} {path}",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            response.text,
            name=f"response {response.status_code}",
            attachment_type=allure.attachment_type.JSON,
        )
        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)
