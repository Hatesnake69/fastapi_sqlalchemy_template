import pytest
import httpx
from tests.test_utils.model_factories.users_factory import create_user
from tests.test_utils.faker import fake
from tests.endpoints.users import URL_PATH


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username",
    [
        123,
        "big_gay_balls",
        "9999-11-11",
        False,
    ],
)
async def test_create_user(client: httpx.AsyncClient, username):
    data = {"username": username, "email": fake.email(), "password_hash": fake.md5()}
    response = await client.post(URL_PATH, json=data)
    result = response.json()
    assert response.status_code == 200
    assert str(result["username"]) == str(data["username"])
