from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import uuid
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
# =========================================================================================


@pytest_asyncio.fixture
async def create_user(client):
    async def _create(username=None, password=None, email=None):
        response = await client.post(
            '/auth/user_register', json={
                "username": username,
                "password": password,
                "email": email})
        assert response.status_code in [200, 201]
        return {
            "username": response.json()['username'],
            'id': response.json()['id'],
            "email": response.json()['email']}
    return _create


@pytest_asyncio.fixture
async def get_token(client, create_user):
    async def _get_token(username=None, password=None, email=None):
        await create_user(username, password, email)

        res = await client.post('/auth/login', data={
            'username': username,
            'password': password
        })
        return res.json()['access_token']

    return _get_token


@pytest_asyncio.fixture
async def auth_header(get_token):
    async def _auth(username=None, password=None, email=None):
        if username is None:
            username = f"user_{uuid.uuid4().hex[:6]}"
        if password is None:
            password = f"pass_{uuid.uuid4().hex[:6]}"
        if email is None:
            email = f"email_{uuid.uuid4().hex[:6]}@email.com"
        token = await get_token(username, password, email)
        return {"Authorization": f"Bearer {token}"}
    return _auth
# =========================================================================================


@pytest_asyncio.fixture
async def create_post(client):
    async def _create_post(header, title=None, content=None, is_published=None):
        if title is None:
            title = f"post_title_{uuid.uuid4().hex[:6]}"
        if content is None:
            content = f"post_content_{uuid.uuid4().hex[:6]}"
        if is_published is None:
            is_published = True

        return await client.post('/post/create_post',
                                 json={
                                     'title': title,
                                     'content': content,
                                     'is_published': is_published
                                 }, headers=header)
    return _create_post

# =========================================================================================


@pytest_asyncio.fixture
async def only_get_token(client):
    async def _get_token(username, password):
        res = await client.post('/auth/login', data={
            'username': username,
            'password': password
        })
        assert res.status_code == 200
        return res.json()['access_token']
    return _get_token
