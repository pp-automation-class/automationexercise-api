"""Wrong HTTP method and missing parameters."""

import allure
import pytest

from helpers.assertions import assert_response

pytestmark = [allure.feature("Negative"), pytest.mark.negative]

NOT_SUPPORTED = "This request method is not supported."


@pytest.mark.parametrize(
    "method, path",
    [
        pytest.param("POST", "/productsList", id="API 2: POST productsList"),
        pytest.param("PUT", "/brandsList", id="API 4: PUT brandsList"),
        pytest.param("DELETE", "/verifyLogin", id="API 9: DELETE verifyLogin"),
    ],
)
def test_method_not_supported(api, method, path):
    assert_response(api.request(method, path), 405, NOT_SUPPORTED)


@allure.title("API 6: search without search_product")
def test_search_without_parameter(api):
    assert_response(
        api.search_product(None),
        400,
        "Bad request, search_product parameter is missing in POST request.",
    )


@allure.title("getUserDetailByEmail without email")
def test_user_detail_without_email(api):
    assert_response(
        api.get_user_detail(None),
        400,
        "Bad request, email parameter is missing in GET request.",
    )


@allure.title("getUserDetailByEmail for an unknown email")
def test_user_detail_unknown_email(api, user):
    assert_response(
        api.get_user_detail(user.email),
        404,
        "Account not found with this email, try another email!",
    )
