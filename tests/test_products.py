"""Products, brands and search."""

import allure
import pytest

from helpers.assertions import assert_response, assert_schema
from schemas.responses import BRANDS_LIST, PRODUCTS_LIST

pytestmark = allure.feature("Products")


@pytest.mark.smoke
@allure.title("API 1: GET all products")
def test_products_list(api):
    body = assert_response(api.products_list(), 200)
    assert_schema(body, PRODUCTS_LIST)
    assert len(body["products"]) > 0

    ids = [p["id"] for p in body["products"]]
    assert len(ids) == len(set(ids)), "product ids must be unique"


@pytest.mark.smoke
@allure.title("API 3: GET all brands")
def test_brands_list(api):
    body = assert_response(api.brands_list(), 200)
    assert_schema(body, BRANDS_LIST)


@allure.title("Every product's brand exists in the brands list")
def test_product_brands_are_known(api):
    brands = {b["brand"] for b in api.brands_list().json()["brands"]}
    products = api.products_list().json()["products"]
    unknown = {p["brand"] for p in products} - brands
    assert not unknown, f"brands missing from /brandsList: {unknown}"


# Data-driven: one test per row. The site matches name OR category, any case.
@pytest.mark.parametrize("term", ["top", "TOP", "jean", "tshirt", "dress", "saree"])
@allure.title("API 5: search '{term}'")
def test_search_product(api, term):
    body = assert_response(api.search_product(term), 200)
    assert_schema(body, PRODUCTS_LIST)
    assert body["products"], f"no results for {term!r}"
    for product in body["products"]:
        text = f"{product['name']} {product['category']['category']}".lower()
        assert term.lower() in text, product


@allure.title("Search with no match returns an empty list")
def test_search_no_results(api):
    body = assert_response(api.search_product("zzzz-no-such-product"), 200)
    assert body["products"] == []
