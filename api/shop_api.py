"""One method per endpoint from https://automationexercise.com/api_list.

Tests call these methods — they never build URLs or form bodies themselves.
Rule: if an endpoint changes, you edit this file, not every test.
"""

import allure
import requests

from api.base_client import BaseClient
from data.user import User


class ShopApi(BaseClient):
    # ---------- products ----------

    @allure.step("GET /productsList")
    def products_list(self) -> requests.Response:
        return self.get("/productsList")

    @allure.step("GET /brandsList")
    def brands_list(self) -> requests.Response:
        return self.get("/brandsList")

    @allure.step("POST /searchProduct '{term}'")
    def search_product(self, term: str | None) -> requests.Response:
        # term=None sends no parameter at all (negative test).
        data = None if term is None else {"search_product": term}
        return self.post("/searchProduct", data=data)

    # ---------- account ----------

    @allure.step("POST /verifyLogin")
    def verify_login(
        self, email: str | None, password: str | None
    ) -> requests.Response:
        # Drop missing fields so we can test "parameter is missing".
        data = {"email": email, "password": password}
        return self.post(
            "/verifyLogin", data={k: v for k, v in data.items() if v is not None}
        )

    @allure.step("POST /createAccount")
    def create_account(self, user: User) -> requests.Response:
        return self.post("/createAccount", data=user.to_form())

    @allure.step("PUT /updateAccount")
    def update_account(self, user: User) -> requests.Response:
        return self.put("/updateAccount", data=user.to_form())

    @allure.step("GET /getUserDetailByEmail {email}")
    def get_user_detail(self, email: str | None) -> requests.Response:
        params = None if email is None else {"email": email}
        return self.get("/getUserDetailByEmail", params=params)

    @allure.step("DELETE /deleteAccount {email}")
    def delete_account(self, email: str, password: str) -> requests.Response:
        return self.delete(
            "/deleteAccount", data={"email": email, "password": password}
        )
