from httpx import AsyncClient


async def test_create_comment_success(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    post = await create_post(header=header)

    response = await client.post('/comment/create_comment',
                                 json={
                                     'is_published': True,
                                     'content': "test_comment",
                                     'post_id': int(post.json()['id'])
                                 }, headers=header)
    assert response.status_code == 200
    assert response.json()['post_id'] == post.json()['id']


async def test_create_comment_success_on_another_user_post(client: AsyncClient,
                                                           auth_header,
                                                           create_post,
                                                           create_comment):
    header = await auth_header()
    post = await create_post(header=header)
    await create_comment(post_id=post.json()['id'], header=header)
    await create_comment(post_id=post.json()['id'], header=header)

    header2 = await auth_header()
    response = await client.post('/comment/create_comment',
                                 json={
                                     'is_published': True,
                                     'content': "test_comment2",
                                     'post_id': int(post.json()['id'])
                                 }, headers=header2)
    await create_comment(post_id=post.json()['id'], header=header2)

    assert response.status_code == 200
    assert response.json()['post_id'] == post.json()['id']

    response = await client.get(f'/comment/get_by_post_id/{post.json()['id']}', headers=header)
    assert response.status_code == 200
    assert len(response.json()) == 4


async def test_create_comment_not_found_post(client: AsyncClient, auth_header, create_post):
    header = await auth_header()

    response = await client.post('/comment/create_comment',
                                 json={
                                     'is_published': True,
                                     'content': "test_comment",
                                     'post_id': 999999
                                 }, headers=header)
    assert response.status_code == 404
    assert response.json()[
        'detail'] == f"Post with ID '{999999}' does not exist."


async def test_get_by_id_success(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    post = await create_post(header=header)
    comment = await create_comment(post_id=post.json()['id'], header=header)

    response = await client.get(f'/comment/get_by_id/{comment.json()['id']}', headers=header)
    assert response.status_code == 200
    assert response.json()['post_id'] == post.json()['id']


async def test_get_by_id_not_found_comment(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()

    response = await client.get(f'/comment/get_by_id/{99999}', headers=header)
    assert response.status_code == 404
    assert response.json()[
        'detail'] == f"Comment with ID '{99999}' does not exist."


async def test_get_by_post_id(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    post = await create_post(header=header)
    await create_comment(post_id=post.json()['id'], header=header)
    await create_comment(post_id=post.json()['id'], header=header)
    await create_comment(post_id=post.json()['id'], header=header)
    await create_comment(post_id=post.json()['id'], header=header)
    await create_comment(post_id=post.json()['id'], header=header)

    response = await client.get(f'/comment/get_by_post_id/{post.json()['id']}', headers=header)
    assert response.status_code == 200
    assert len(response.json()) == 5


async def test_get_by_post_id_no_comment(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    post = await create_post(header=header)

    response = await client.get(f'/comment/get_by_post_id/{post.json()['id']}', headers=header)
    assert response.status_code == 200
    assert len(response.json()) == 0


async def test_get_by_post_id_not_found_post(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()

    response = await client.get(f'/comment/get_by_post_id/{99999}', headers=header)
    assert response.status_code == 404
    assert response.json()[
        'detail'] == f"Post with ID '{99999}' does not exist."


async def test_update_success(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    post = await create_post(header=header)
    comment = await create_comment(post_id=post.json()['id'], header=header)

    response = await client.put(f'/comment/update/{comment.json()['id']}',
                                json={
                                    "content": "updated_content",
                                    "is_published": False
    }, headers=header)
    assert response.status_code == 200
    assert response.json() is True


async def test_update_not_found_comment(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    await create_post(header=header)

    response = await client.put(f'/comment/update/{99999}',
                                json={
                                    "content": "updated_content",
                                    "is_published": False
    }, headers=header)
    assert response.status_code == 404
    assert response.json()[
        'detail'] == f"Comment with ID '{99999}' does not exist."


async def test_update_invalid_authentication(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    post = await create_post(header=header)
    comment = await create_comment(post_id=post.json()['id'], header=header)

    header2 = await auth_header()

    response = await client.put(f'/comment/update/{comment.json()['id']}',
                                json={
                                    "content": "updated_content",
                                    "is_published": False
    }, headers=header2)
    assert response.status_code == 401
    assert f"Comment with ID '{comment.json()['id']} does not belong to user" in response.json()[
        'detail']


async def test_delete_success(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    post = await create_post(header=header)
    comment = await create_comment(post_id=post.json()['id'], header=header)

    response = await client.get(f'/comment/get_by_id/{comment.json()['id']}', headers=header)
    assert response.status_code == 200
    assert response.json()['post_id'] == post.json()['id']

    response = await client.delete(f'/comment/delete/{comment.json()['id']}',
                                   headers=header)
    assert response.status_code == 200

    response = await client.get(f'/comment/get_by_id/{comment.json()['id']}', headers=header)
    assert response.status_code == 404
    assert response.json()[
        'detail'] == f"Comment with ID '{comment.json()['id']}' does not exist."


async def test_delete_not_found_comment(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    await create_post(header=header)

    response = await client.delete(f'/comment/delete/{99999}',
                                   headers=header)
    assert response.status_code == 404
    assert response.json()[
        'detail'] == f"Comment with ID '{99999}' does not exist."


async def test_delete_invalid_authentication(client: AsyncClient, auth_header, create_post, create_comment):
    header = await auth_header()
    post = await create_post(header=header)
    comment = await create_comment(post_id=post.json()['id'], header=header)

    header2 = await auth_header()

    response = await client.delete(f'/comment/delete/{comment.json()['id']}',
                                   headers=header2)

    assert f"Comment with ID '{comment.json()['id']} does not belong to user" in response.json()[
        'detail']
    assert response.status_code == 401
