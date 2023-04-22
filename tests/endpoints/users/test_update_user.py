import pytest
import httpx
from tests.test_utils.model_factories.users_factory import create_user
from tests.test_utils.faker import fake
from tests.endpoints.users import URL_PATH


@pytest.mark.asyncio
async def test_update_user(client: httpx.AsyncClient):
    user = await create_user(username=fake.name())
    data = {"username": fake.name()}
    response = await client.patch(f"{URL_PATH}{user.id}", json=data)
    result = response.json()
    assert response.status_code == 200
    assert str(result["username"]) == str(data["username"])
    assert str(user.username) != str(result["username"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "param",
    [
        "big_gay_balls",
        "9999-11-11",
        False,
    ],
)
async def test_update_user_invalid_id(client: httpx.AsyncClient, param):
    await create_user(username=fake.name())
    data = {"username": fake.name()}
    response = await client.patch(f"{URL_PATH}{param}", json=data)
    assert response.status_code == 404
