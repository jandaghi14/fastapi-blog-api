import uuid
from httpx import AsyncClient


async def test_user_register_endpoint_success(client: AsyncClient):
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = f"pass_{uuid.uuid4().hex[:6]}"
    email = f"email_{uuid.uuid4().hex[:6]}@email.com"
    response = await client.post("/auth/user_register",
                                 json={"username": username,
                                       "password": password,
                                       "email": email
                                       })

    assert response.status_code == 200
    assert response.json()['username'] == username


async def test_user_register_endpoint_already_exist_user(client: AsyncClient):
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = f"pass_{uuid.uuid4().hex[:6]}"
    email = f"email_{uuid.uuid4().hex[:6]}@email.com"
    await client.post("/auth/user_register",
                      json={"username": username,
                            "password": "randonipass",
                            "email": "randomemailo"
                            })
    response = await client.post("/auth/user_register",
                                 json={"username": username,
                                       "password": password,
                                       "email": email
                                       })

    assert response.status_code == 400
    assert response.json()[
        "detail"] == f"Username '{username}' already exists!"


async def test_user_login_endpoint_success(client: AsyncClient):
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = f"pass_{uuid.uuid4().hex[:6]}"
    email = f"email_{uuid.uuid4().hex[:6]}@email.com"
    await client.post("/auth/user_register",
                      json={"username": username,
                            "password": password,
                            "email": email
                            })

    response = await client.post("/auth/login",
                                 data={'username': username,
                                       "password": password}
                                 )

    assert response.status_code == 200
    assert response.json()['access_token'] != False


async def test_user_login_endpoint_wrong_username(client: AsyncClient):
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = f"pass_{uuid.uuid4().hex[:6]}"
    email = f"email_{uuid.uuid4().hex[:6]}@email.com"
    await client.post("/auth/user_register",
                      json={"username": username,
                            "password": password,
                            "email": email
                            })

    response = await client.post("/auth/login",
                                 data={'username': 'false_username',
                                       "password": password}
                                 )

    assert response.status_code == 400
    assert response.json()['detail'] == "Wrong username"


async def test_user_login_endpoint_wrong_password(client: AsyncClient):
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = f"pass_{uuid.uuid4().hex[:6]}"
    email = f"email_{uuid.uuid4().hex[:6]}@email.com"
    await client.post("/auth/user_register",
                      json={"username": username,
                            "password": password,
                            "email": email
                            })

    response = await client.post("/auth/login",
                                 data={'username': username,
                                       "password": 'wronge_password'}
                                 )

    assert response.status_code == 401
    assert response.json()['detail'] == "username or password is wrong"
