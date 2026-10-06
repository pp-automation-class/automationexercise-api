"""POST /verifyLogin — one real account, many input combinations."""

import allure
import pytest

from helpers.assertions import assert_response

pytestmark = allure.feature("Login")

MISSING = "Bad request, email or password parameter is missing in POST request."


@pytest.mark.smoke
@pytest.mark.account
@allure.title("API 7: valid email + password")
def test_verify_login_valid(api, registered_user):
    response = api.verify_login(registered_user.email, registered_user.password)
    assert_response(response, 200, "User exists!")


# Data-driven: each row is (what to send, expected code, expected message).
# "valid" = take the value from the real account; None = do not send the field.
@pytest.mark.negative
@pytest.mark.account
@pytest.mark.parametrize(
    "email, password, code, message",
    [
        pytest.param(None, "valid", 400, MISSING, id="API 8: missing email"),
        pytest.param("valid", None, 400, MISSING, id="missing password"),
        pytest.param(
            "valid", "wrong-pass", 404, "User not found!", id="wrong password"
        ),
        pytest.param(
            "nobody@example.com",
            "valid",
            404,
            "User not found!",
            id="API 10: unknown email",
        ),
        pytest.param(
            "VALID", "valid", 404, "User not found!", id="email in upper case"
        ),
    ],
)
def test_verify_login_invalid(api, registered_user, email, password, code, message):
    real = registered_user
    email = {"valid": real.email, "VALID": real.email.upper()}.get(email, email)
    password = real.password if password == "valid" else password
    assert_response(api.verify_login(email, password), code, message)
