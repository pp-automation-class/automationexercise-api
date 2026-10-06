"""Account lifecycle: create -> read -> update -> delete."""

import allure
import pytest

from helpers.assertions import assert_response, assert_schema
from schemas.responses import USER_DETAIL

pytestmark = [allure.feature("Account"), pytest.mark.account]


@allure.title("API 11: create account")
def test_create_account(api, user):
    try:
        assert_response(api.create_account(user), 201, "User created!")
    finally:
        api.delete_account(user.email, user.password)


@pytest.mark.negative
@allure.title("Create account with an email that already exists")
def test_create_account_duplicate_email(api, registered_user):
    assert_response(api.create_account(registered_user), 400, "Email already exists!")


@allure.title("API 14: user details match what was sent")
def test_get_user_detail(api, registered_user):
    body = assert_response(api.get_user_detail(registered_user.email), 200)
    assert_schema(body, USER_DETAIL)

    saved = body["user"]
    # The API renames some fields: firstname -> first_name, birth_date -> birth_day.
    expected = {
        "name": registered_user.name,
        "email": registered_user.email,
        "title": registered_user.title,
        "birth_day": registered_user.birth_date,
        "birth_month": registered_user.birth_month,
        "birth_year": registered_user.birth_year,
        "first_name": registered_user.firstname,
        "last_name": registered_user.lastname,
        "company": registered_user.company,
        "address1": registered_user.address1,
        "country": registered_user.country,
        "state": registered_user.state,
        "city": registered_user.city,
        "zipcode": registered_user.zipcode,
    }
    assert {k: saved[k] for k in expected} == expected
    assert "password" not in saved, "API must never return the password"


@allure.title("API 13: update account")
def test_update_account(api, registered_user):
    changed = registered_user.with_changes(name="Updated Name", city="Toronto")
    assert_response(api.update_account(changed), 200, "User updated!")

    saved = api.get_user_detail(changed.email).json()["user"]
    assert (saved["name"], saved["city"]) == ("Updated Name", "Toronto")


@allure.title("API 12: delete account, then it is gone")
def test_delete_account(api, registered_user):
    response = api.delete_account(registered_user.email, registered_user.password)
    assert_response(response, 200, "Account deleted!")

    assert_response(api.get_user_detail(registered_user.email), 404)
    assert_response(
        api.delete_account(registered_user.email, registered_user.password),
        404,
        "Account not found!",
    )
