"""JSON Schemas for successful responses.

A schema catches a renamed/missing field or a wrong type on every item,
which a few hand-written asserts would miss.
"""

PRODUCT = {
    "type": "object",
    "required": ["id", "name", "price", "brand", "category"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string", "minLength": 1},
        "price": {"type": "string", "pattern": r"^Rs\. \d+$"},
        "brand": {"type": "string"},
        "category": {
            "type": "object",
            "required": ["usertype", "category"],
            "properties": {
                "usertype": {
                    "type": "object",
                    "required": ["usertype"],
                    "properties": {"usertype": {"type": "string"}},
                },
                "category": {"type": "string"},
            },
        },
    },
}

PRODUCTS_LIST = {
    "type": "object",
    "required": ["responseCode", "products"],
    "properties": {
        "responseCode": {"const": 200},
        "products": {"type": "array", "items": PRODUCT},
    },
}

BRANDS_LIST = {
    "type": "object",
    "required": ["responseCode", "brands"],
    "properties": {
        "responseCode": {"const": 200},
        "brands": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "brand"],
                "properties": {
                    "id": {"type": "integer"},
                    "brand": {"type": "string", "minLength": 1},
                },
            },
        },
    },
}

USER_DETAIL = {
    "type": "object",
    "required": ["responseCode", "user"],
    "properties": {
        "responseCode": {"const": 200},
        "user": {
            "type": "object",
            "required": [
                "id",
                "name",
                "email",
                "title",
                "first_name",
                "last_name",
                "country",
                "state",
                "city",
                "zipcode",
            ],
            "properties": {"id": {"type": "integer"}, "email": {"type": "string"}},
        },
    },
}
