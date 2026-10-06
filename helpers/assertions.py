"""Shared response checks.

This API always answers HTTP 200. The real status lives in the JSON body:
    {"responseCode": 404, "message": "User not found!"}
So every test checks both.
"""

import allure
import requests
from jsonschema import validate


@allure.step("Expect responseCode {code}")
def assert_response(
    response: requests.Response, code: int, message: str | None = None
) -> dict:
    """Check HTTP 200 + body responseCode (+ message). Return the parsed body."""
    assert response.status_code == 200, f"HTTP {response.status_code}: {response.text}"
    body = response.json()
    assert body["responseCode"] == code, body
    if message is not None:
        assert body["message"] == message, body
    return body


@allure.step("Validate JSON schema")
def assert_schema(body: dict, schema: dict) -> None:
    validate(instance=body, schema=schema)
