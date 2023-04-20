import sys

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.user}:{settings.password}@"
    f"{settings.host}:{settings.port}/"
    f"{settings.name}"
)
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.test_user}:{settings.test_password}@"
    f"{settings.test_host}:{settings.test_port}/"
    f"{settings.test_name}"
)

if "pytest" in sys.argv[0]:
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
else:
    engine = create_async_engine(DATABASE_URL, future=True, echo=True)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
