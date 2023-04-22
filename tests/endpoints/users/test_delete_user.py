import pytest
import httpx
from tests.test_utils.model_factories.users_factory import create_user
from tests.test_utils.faker import fake
from tests.endpoints.users import URL_PATH


@pytest.mark.asyncio
async def test_delete_user(client: httpx.AsyncClient):
    user = await create_user(username=fake.name())
    response = await client.delete(
        f"{URL_PATH}{user.id}",
    )
    result = response.json()
    assert response.status_code == 200
    assert str(result["username"]) == str(user.username)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "id",
    [
        "big_gay_balls",
        "9999-11-11",
        False,
    ],
)
async def test_delete_username_invalid_id(client: httpx.AsyncClient, id):
    response = await client.delete(f"{URL_PATH}{id}")
    assert response.status_code == 404
