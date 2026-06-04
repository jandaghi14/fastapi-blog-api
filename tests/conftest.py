from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.core.config import settings
from app.db.base import Base
from app.db import all_models
from app.main import app
from app.db.session import get_db
# echo=True on the engine during development.
# It prints every SQL query SQLAlchemy generates to the terminal.
# Invaluable for debugging async queries.
engine = create_async_engine(settings.TEST_DATABASE_URL, echo=True)
LocalSession = async_sessionmaker(engine)


async def override_get_db():
    session = LocalSession()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def client():
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:

        yield ac

    app.dependency_overrides = {}
