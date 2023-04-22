import pytest
import httpx
from tests.test_utils.model_factories.users_factory import create_user
from tests.test_utils.faker import fake
from tests.endpoints.users import URL_PATH


@pytest.mark.asyncio
async def test_get_users_without_params(client: httpx.AsyncClient):
    await create_user(username=fake.name())
    response = await client.get(
        f"{URL_PATH}",
    )
    result = response.json()
    assert len(result) > 0
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_users_limit_offset(client: httpx.AsyncClient):
    for _ in range(10):
        await create_user(username=fake.name())
    response = await client.get(f"{URL_PATH}", params={"limit": 5, "offset": 5})
    result = response.json()
    assert len(result) == 5
    assert response.status_code == 200
