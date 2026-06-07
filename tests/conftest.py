from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
import uuid
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.core.config import settings
from app.db.base import Base

from app.main import app
from app.db.session import get_db

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


@pytest_asyncio.fixture(autouse=True)
async def clear_tables():
    yield
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE posts, users, comments, posts_tags, tags RESTART IDENTITY CASCADE"))

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


@pytest_asyncio.fixture
async def admin_auth_header(client, only_get_token):
    async def _admin():
        async with LocalSession() as session:
            from app.models.model_user import User
            from app.core.security import hash_password
            username = f"admin_{uuid.uuid4().hex[:6]}"
            password = f"pass_{uuid.uuid4().hex[:6]}"
            admin = User(
                username=username,
                email=f"{username}@email.com",
                password=hash_password(password),
                role="admin",
                is_active=True
            )
            session.add(admin)
            await session.commit()
        token = await only_get_token(username, password)
        return {"Authorization": f"Bearer {token}"}
    return _admin
# =========================================================================================


@pytest_asyncio.fixture()
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


@pytest_asyncio.fixture()
async def create_comment(client):
    async def _create_comment(header, post_id, content=None, is_published=None):
        if content is None:
            content = f"comment_content_{uuid.uuid4().hex[:6]}"
        if is_published is None:
            is_published = True

        return await client.post('/comment/create_comment',
                                 json={
                                     'post_id': post_id,
                                     'content': content,
                                     'is_published': is_published
                                 }, headers=header)
    return _create_comment


@pytest_asyncio.fixture()
async def create_tag(client):
    async def _create_tag(header, name=None):
        if name is None:
            name = f"tag_name_{uuid.uuid4().hex[:6]}"

        return await client.post('/tag/create_tag', params={'name': name}, headers=header)
    return _create_tag


@pytest_asyncio.fixture()
async def assign_tag_to_post(client):
    async def _assign_tag_to_post(header, tag_id, post_id):

        return await client.post("/tag/assign_tag_to_post",
                                 params={
                                     'tag_id': tag_id,
                                     'post_id': post_id
                                 }, headers=header)
    return _assign_tag_to_post


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
