"""Test user built with Faker. A new unique email every call."""

from dataclasses import asdict, dataclass, replace
from uuid import uuid4

from faker import Faker

_fake = Faker()


@dataclass(frozen=True)
class User:
    name: str
    email: str
    password: str
    title: str
    birth_date: str
    birth_month: str
    birth_year: str
    firstname: str
    lastname: str
    company: str
    address1: str
    address2: str
    country: str
    zipcode: str
    state: str
    city: str
    mobile_number: str

    def to_form(self) -> dict[str, str]:
        """Body for createAccount / updateAccount (form fields, not JSON)."""
        return asdict(self)

    def with_changes(self, **fields) -> "User":
        """Copy with some fields changed — used by the update test."""
        return replace(self, **fields)


def build_user() -> User:
    first, last = _fake.first_name(), _fake.last_name()
    birth = _fake.date_of_birth(minimum_age=18, maximum_age=80)
    return User(
        name=f"{first} {last}",
        # uuid keeps the email unique even if Faker repeats a name.
        email=f"qa_{uuid4().hex[:12]}@example.com",
        password=_fake.password(length=12),
        title=_fake.random_element(["Mr", "Mrs"]),
        birth_date=str(birth.day),
        birth_month=str(birth.month),
        birth_year=str(birth.year),
        firstname=first,
        lastname=last,
        company=_fake.company(),
        address1=_fake.street_address(),
        address2="",
        # The site's signup form only offers a fixed country list.
        country=_fake.random_element(["United States", "Canada", "Australia"]),
        zipcode=_fake.postcode(),
        state=_fake.state(),
        city=_fake.city(),
        mobile_number=_fake.numerify("##########"),
    )
