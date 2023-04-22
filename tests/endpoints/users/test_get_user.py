import pytest
import httpx
from tests.test_utils.model_factories.users_factory import create_user
from tests.test_utils.faker import fake
from tests.endpoints.users import URL_PATH


@pytest.mark.asyncio
async def test_get_user(client: httpx.AsyncClient):
    user = await create_user(username=fake.name())
    response = await client.get(
        f"{URL_PATH}{user.id}",
    )
    result = response.json()
    assert response.status_code == 200
    assert str(result["username"]) == str(user.username)
