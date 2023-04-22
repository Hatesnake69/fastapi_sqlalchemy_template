import asyncio

from typing import AsyncGenerator, Iterator

import pytest_asyncio

from httpx import AsyncClient
from sqlalchemy import create_engine

from config import settings
from main import app
from models.base_model import Base


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://localhost:8000/") as cli:
        yield cli


@pytest_asyncio.fixture(scope="session")
def event_loop() -> Iterator[asyncio.events.AbstractEventLoop]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
def create_db():
    engine = create_engine(
        f"postgresql://"
        f"{settings.test_user}:{settings.test_password}@"
        f"{settings.test_host}:{settings.test_port}/"
        f"{settings.test_name}"
    )
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
