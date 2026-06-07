import uuid
from httpx import AsyncClient


async def test_post_create_endpoint_success(client: AsyncClient, auth_header):
    header = await auth_header()
    response = await client.post('/post/create_post',
                                 json={'title': 'test_title',
                                       'content': 'test_content',
                                       'is_published': True

                                       }, headers=header)
    assert response.status_code == 200


async def test_post_get_all_posts_endpoint_success(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)

    response = await client.get('/post/get_all_posts', headers=header)
    assert response.status_code == 200
    assert response.json()['total'] == 4
    assert response.json()['page'] == 1
    assert response.json()['pages'] == 1
    assert response.json()['size'] == 5


async def test_post_get_all_posts_pagination(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)

    response = await client.get('/post/get_all_posts',
                                params={'page': 1, 'size': 2},
                                headers=header)
    assert response.status_code == 200
    assert response.json()['total'] == 4
    assert response.json()['page'] == 1
    assert response.json()['pages'] == 2
    assert response.json()['size'] == 2


async def test_post_get_all_posts_endpoint_without_post(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    response = await client.get('/post/get_all_posts', headers=header)
    assert response.status_code == 200
    assert response.json()['items'] == []


async def test_post_get_post_by_id_endpoint_success(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    post1 = await create_post(header=header)
    post2 = await create_post(header=header)
    post3 = await create_post(header=header)
    post4 = await create_post(header=header)
    response = await client.get(f'/post/get_post_by_id/{post2.json()['id']}', headers=header)
    assert response.status_code == 200
    assert response.json()['id'] == post2.json()['id']


async def test_post_get_post_by_id_endpoint_not_found(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    response = await client.get(f'/post/get_post_by_id/{1}', headers=header)
    assert response.status_code == 404
    assert response.json()['detail'] == "The post does not exist for the user"


async def test_post_get_post_by_id_endpoint_not_owner_user(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    post1 = await create_post(header=header)

    header2 = await auth_header()
    response = await client.get(f'/post/get_post_by_id/{post1.json()['id']}', headers=header2)
    assert response.status_code == 200
    assert response.json()['owner_id'] == post1.json()['owner_id']


async def test_post_search_endpoint(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    title = f"post_title_keyword_search_title"
    content = f"post_content_keyword_search_content"
    is_published = True
    post1 = await create_post(title=title, content=content, is_published=is_published, header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)

    response = await client.get('/post/search',
                                params={
                                    'title': 'keyword_search_title'
                                },
                                headers=header
                                )

    assert response.status_code == 200
    assert response.json()[0]['title'] == title

    response = await client.get('/post/search',
                                params={
                                    "is_published": True
                                },
                                headers=header
                                )

    assert response.status_code == 200
    assert len(response.json()) == 7


async def test_post_search_endpoint_no_matching(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    title = f"post_title_keyword_search_title"
    content = f"post_content_keyword_search_content"
    is_published = True
    post1 = await create_post(title=title, content=content, is_published=is_published, header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)
    await create_post(header=header)

    response = await client.get('/post/search',
                                params={
                                    'title': 'python_learning'
                                },
                                headers=header
                                )

    assert response.status_code == 200
    assert response.json() == []


async def test_post_update_success_owner(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    title = f"post_title_{uuid.uuid4().hex[:6]}"
    content = f"post_content_{uuid.uuid4().hex[:6]}"
    is_published = True
    post1 = await create_post(title=title, content=content, is_published=is_published, header=header)

    response = await client.put(f'/post/update_post/{post1.json()['id']}',
                                json={
        'title': "updated_title",
        'content': "updated_content",
        'is_published': False},
        headers=header)

    assert response.status_code == 200
    assert response.json()[
        'message'] == f"Post with ID '{post1.json()['id']}' updated successfully!"


async def test_post_update_success_admin(client: AsyncClient, auth_header, create_post, admin_auth_header):
    header = await auth_header()
    title = f"post_title_{uuid.uuid4().hex[:6]}"
    content = f"post_content_{uuid.uuid4().hex[:6]}"
    is_published = True
    post1 = await create_post(title=title, content=content, is_published=is_published, header=header)

    header_admin = await admin_auth_header()

    response = await client.put(f'/post/update_post/{post1.json()['id']}',
                                json={
        'title': "updated_title",
        'content': "updated_content",
        'is_published': False},
        headers=header_admin)

    assert response.status_code == 200
    assert response.json()[
        'message'] == f"Post with ID '{post1.json()['id']}' updated successfully!"

    response = await client.get(f'/post/get_post_by_id/{post1.json()['id']}', headers=header)
    assert response.status_code == 200
    assert response.json()['title'] == "updated_title"
    assert response.json()['content'] == "updated_content"
    assert response.json()['is_published'] == False


async def test_post_update_invalid_user(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    title = f"post_title_{uuid.uuid4().hex[:6]}"
    content = f"post_content_{uuid.uuid4().hex[:6]}"
    is_published = True
    post1 = await create_post(title=title, content=content, is_published=is_published, header=header)

    header2 = await auth_header()

    response = await client.put(f'/post/update_post/{post1.json()['id']}',
                                json={
        'title': "updated_title",
        'content': "updated_content",
        'is_published': False},
        headers=header2)

    assert response.status_code == 401
    assert f"Post with ID {post1.json()['id']} does not belong to User" in response.json()[
        'detail']


async def test_post_delete_success(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    post1 = await create_post(header=header)

    response = await client.get(f'/post/get_post_by_id/{post1.json()['id']}', headers=header)
    assert response.status_code == 200
    assert response.json()['id'] == post1.json()['id']

    response = await client.delete(f'/post/delete_post/{post1.json()['id']}',
                                   headers=header)

    assert response.status_code == 200
    assert response.json()[
        'message'] == f"Post with ID '{post1.json()['id']}' deleted successfully!"


async def test_post_delete_admin_success(client: AsyncClient, auth_header, create_post, admin_auth_header):
    header = await auth_header()
    post1 = await create_post(header=header)
    header_admin = await admin_auth_header()

    response = await client.get(f'/post/get_post_by_id/{post1.json()['id']}', headers=header)
    assert response.status_code == 200
    assert response.json()['id'] == post1.json()['id']

    response = await client.delete(f'/post/delete_post/{post1.json()['id']}',
                                   headers=header_admin)

    assert response.status_code == 200
    assert response.json()[
        'message'] == f"Post with ID '{post1.json()['id']}' deleted successfully!"

    response = await client.get(f'/post/get_post_by_id/{post1.json()['id']}', headers=header)
    assert response.status_code == 404
    assert response.json()['detail'] == "The post does not exist for the user"


async def test_post_delete_invalid_user(client: AsyncClient, auth_header, create_post):
    header = await auth_header()
    post1 = await create_post(header=header)
    response = await client.get(f'/post/get_post_by_id/{post1.json()['id']}', headers=header)
    assert response.status_code == 200
    assert response.json()['id'] == post1.json()['id']

    header2 = await auth_header()
    response = await client.delete(f'/post/delete_post/{post1.json()['id']}',
                                   headers=header2)

    assert response.status_code == 401
    assert f"Post with ID {post1.json()['id']} does not belong to User" in response.json()[
        'detail']

    response = await client.get(f'/post/get_post_by_id/{post1.json()['id']}', headers=header)
    assert response.status_code == 200
    assert response.json()['id'] == post1.json()['id']


async def test_post_search_tag_title_success_on_both(client: AsyncClient, auth_header, create_post, create_tag, assign_tag_to_post):
    header = await auth_header()
    post1 = await create_post(title='title1', header=header)
    post2 = await create_post(title='subject2', header=header)
    post3 = await create_post(title='desc3', header=header)
    tag1 = await create_tag(name="tag1", header=header)
    tag2 = await create_tag(name="tag2", header=header)
    tag3 = await create_tag(name="tag3", header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post1.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post2.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post3.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag2.json()['id'], post_id=post1.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag2.json()['id'], post_id=post2.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag3.json()['id'], post_id=post3.json()['id'], header=header)

    response = await client.get(f"/post/search_tag_title",
                                params={'tag': tag1.json()['name'],
                                        'title': "title1"},
                                headers=header)
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_post_search_tag_title_success_on_tag(client: AsyncClient, auth_header, create_post, create_tag, assign_tag_to_post):
    header = await auth_header()
    post1 = await create_post(title='title1', header=header)
    post2 = await create_post(title='subject2', header=header)
    post3 = await create_post(title='desc3', header=header)
    tag1 = await create_tag(name="tag1", header=header)
    tag2 = await create_tag(name="tag2", header=header)
    tag3 = await create_tag(name="tag3", header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post1.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post2.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post3.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag2.json()['id'], post_id=post1.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag2.json()['id'], post_id=post2.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag3.json()['id'], post_id=post3.json()['id'], header=header)
    response = await client.get(f"/post/search_tag_title",
                                params={'tag': tag1.json()['name'],
                                        'title': None
                                        },
                                headers=header)
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_post_search_tag_title_success_on_title(client: AsyncClient, auth_header, create_post, create_tag, assign_tag_to_post):
    header = await auth_header()
    post1 = await create_post(title='title1', header=header)
    post2 = await create_post(title='subject2', header=header)
    post3 = await create_post(title='desc3', header=header)
    tag1 = await create_tag(name="tag1", header=header)
    tag2 = await create_tag(name="tag2", header=header)
    tag3 = await create_tag(name="tag3", header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post1.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post2.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag1.json()['id'], post_id=post3.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag2.json()['id'], post_id=post1.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag2.json()['id'], post_id=post2.json()['id'], header=header)
    await assign_tag_to_post(tag_id=tag3.json()['id'], post_id=post3.json()['id'], header=header)
    response = await client.get(f"/post/search_tag_title",
                                params={
                                    'title': 'title1'
                                },
                                headers=header)
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_post_search_tag_title_not_found(client: AsyncClient, auth_header, create_post, create_tag, assign_tag_to_post):
    header = await auth_header()

    response = await client.get(f"/post/search_tag_title",

                                headers=header)
    assert response.status_code == 400
    assert response.json()[
        'detail'] == "Provide at least a title or a tag to search."
