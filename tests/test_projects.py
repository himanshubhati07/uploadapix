# Project endpoint tests.
import pytest
from tests.utils.factories import user_payload, login_payload, project_payload


async def get_token(client):
    payload = user_payload("-projects")
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json=login_payload(payload["email"]))
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_create_list_get_update_project(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post("/api/v1/projects", json=project_payload(), headers=headers)
    assert create_resp.status_code == 201
    project_id = create_resp.json()["id"]

    list_resp = await client.get("/api/v1/projects", headers=headers)
    assert list_resp.status_code == 200

    get_resp = await client.get(f"/api/v1/projects/{project_id}", headers=headers)
    assert get_resp.status_code == 200

    update_resp = await client.put(
        f"/api/v1/projects/{project_id}",
        json={"name": "Updated Project"},
        headers=headers,
    )
    assert update_resp.status_code == 200
