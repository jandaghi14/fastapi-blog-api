from httpx import AsyncClient


async def test_create_tag_success(client: AsyncClient, auth_header):
    header = await auth_header()
    response = await client.post('/tag/create_tag', params={'name': 'test_tag'}, headers=header)
    assert response.status_code == 200
    assert response.json()['name'] == 'test_tag'


async def test_create_tag_already_exists(client: AsyncClient, auth_header):
    header = await auth_header()
    await client.post('/tag/create_tag', params={'name': 'test_tag'}, headers=header)
    response = await client.post('/tag/create_tag', params={'name': 'test_tag'}, headers=header)
    assert response.status_code == 400
    assert response.json()[
        'detail'] == "Tag with name 'test_tag' already exist."


async def test_get_all_tags(client: AsyncClient, auth_header, create_tag):
    header = await auth_header()
    await create_tag(header=header)
    await create_tag(header=header)
    await create_tag(header=header)
    await create_tag(header=header)
    response = await client.get("/tag/get_all", headers=header)
    assert len(response.json()) == 4
    assert response.status_code == 200


async def test_get_all_tags_no_tags(client: AsyncClient, auth_header):
    header = await auth_header()

    response = await client.get("/tag/get_all", headers=header)
    assert len(response.json()) == 0
    assert response.status_code == 200


async def test_get_by_id_tag(client: AsyncClient, auth_header, create_tag):
    header = await auth_header()
    await create_tag(header=header)
    await create_tag(header=header)
    tag1 = await create_tag(name='test_tag', header=header)
    await create_tag(header=header)

    response = await client.get(f"/tag/get_by_id/{tag1.json()['id']}", headers=header)
    assert response.json()['name'] == 'test_tag'
    assert response.json()['id'] == tag1.json()['id']
    assert response.status_code == 200


async def test_get_by_id_not_found_tag(client: AsyncClient, auth_header):
    header = await auth_header()

    response = await client.get(f"/tag/get_by_id/{99999}", headers=header)
    assert response.json()['detail'] == f"Tag with ID '{99999}' not found."
    assert response.status_code == 404


async def test_update_success(client: AsyncClient, auth_header, create_tag):
    header = await auth_header()
    tag1 = await create_tag(header=header)

    response = await client.put("/tag/update",
                                params={'tag_id': tag1.json(
                                )['id'], 'new_tag': 'updated_tag'},
                                headers=header)
    assert response.json() is True
    assert response.status_code == 200
    response = await client.get(f"/tag/get_by_id/{tag1.json()['id']}", headers=header)
    assert response.json()['name'] == 'updated_tag'
    assert response.json()['id'] == tag1.json()['id']
    assert response.status_code == 200


async def test_update_not_found_tag(client: AsyncClient, auth_header, create_tag):
    header = await auth_header()
    tag1 = 99999

    response = await client.put("/tag/update",
                                params={'tag_id': tag1,
                                        'new_tag': 'updated_tag'},
                                headers=header)
    assert response.json()['detail'] == f"Tag with ID '{tag1}' not found."
    assert response.status_code == 404


async def test_delete_success(client: AsyncClient, auth_header, create_tag):
    header = await auth_header()
    tag1 = await create_tag(header=header)

    response = await client.delete(f"/tag/delete/{tag1.json()['id']}",
                                   headers=header)
    assert response.json() is True

    response = await client.get("/tag/get_all", headers=header)
    assert response.json() == []
    assert response.status_code == 200


async def test_assign_tag_to_post_success(client: AsyncClient, auth_header, create_tag, create_post):
    header = await auth_header()
    post1 = await create_post(header=header)
    tag1 = await create_tag(header=header)

    response = await client.post("/tag/assign_tag_to_post",
                                 params={
                                     'tag_id': tag1.json()['id'],
                                     'post_id': post1.json()['id']
                                 }, headers=header)

    assert response.json()['tag_id'] == tag1.json()['id']
    assert response.json()['post_id'] == post1.json()['id']
    assert response.status_code == 200


async def test_assign_tag_to_post_not_found_tag(client: AsyncClient, auth_header, create_tag, create_post):
    header = await auth_header()
    post1 = await create_post(header=header)
    tag1 = 99999

    response = await client.post("/tag/assign_tag_to_post",
                                 params={
                                     'tag_id': tag1,
                                     'post_id': post1.json()['id']
                                 }, headers=header)

    assert response.json()['detail'] == "Either tag or id does not exist."
    assert response.status_code == 404


async def test_assign_tag_to_post_not_found_post(client: AsyncClient, auth_header, create_tag, create_post):
    header = await auth_header()
    post1 = 99999
    tag1 = await create_tag(header=header)

    response = await client.post("/tag/assign_tag_to_post",
                                 params={
                                     'tag_id': tag1.json()['id'],
                                     'post_id': post1
                                 }, headers=header)

    assert response.json()['detail'] == "Either tag or id does not exist."
    assert response.status_code == 404


async def test_remove_tag_from_post_success(client: AsyncClient, auth_header, create_tag, create_post):
    header = await auth_header()
    post1 = await create_post(header=header)
    tag1 = await create_tag(header=header)

    await client.post("/tag/assign_tag_to_post",
                      params={
                          'tag_id': tag1.json()['id'],
                          'post_id': post1.json()['id']
                      }, headers=header)

    response = await client.delete("/tag/remove_tag_from_post",
                                   params={
                                       'tag_id': tag1.json()['id'],
                                       'post_id': post1.json()['id']},
                                   headers=header)

    assert response.json() is True
    assert response.status_code == 200


async def test_remove_tag_from_post_not_found_tag_post(client: AsyncClient, auth_header, create_tag, create_post):
    header = await auth_header()

    response = await client.delete("/tag/remove_tag_from_post",
                                   params={
                                       'tag_id': 99999,
                                       'post_id': 99999},
                                   headers=header)

    assert response.json()['detail'] == "Tag-post assignment not found."
    assert response.status_code == 404


async def test_remove_tag_from_post_not_found_tag(client: AsyncClient, auth_header, create_tag, create_post):
    header = await auth_header()
    post1 = await create_post(header=header)
    response = await client.delete("/tag/remove_tag_from_post",
                                   params={
                                       'tag_id': 99999,
                                       'post_id': post1.json()['id']},
                                   headers=header)

    assert response.json()['detail'] == "Tag-post assignment not found."
    assert response.status_code == 404


async def test_remove_tag_from_post_not_found_post(client: AsyncClient, auth_header, create_tag, create_post):
    header = await auth_header()
    tag1 = await create_tag(header=header)

    response = await client.delete("/tag/remove_tag_from_post",
                                   params={
                                       'tag_id': tag1.json()['id'],
                                       'post_id': 99999},
                                   headers=header)

    assert response.json()['detail'] == "Tag-post assignment not found."
