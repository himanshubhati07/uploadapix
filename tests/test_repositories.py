# Repository endpoint tests.
import pytest
from tests.utils.factories import user_payload, login_payload, repository_payload


async def get_token(client):
    payload = user_payload("-repos")
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json=login_payload(payload["email"]))
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_create_get_update_repository(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post("/api/v1/repositories", json=repository_payload(), headers=headers)
    assert create_resp.status_code == 201
    repo_id = create_resp.json()["id"]

    get_resp = await client.get(f"/api/v1/repositories/{repo_id}", headers=headers)
    assert get_resp.status_code == 200

    update_resp = await client.put(
        f"/api/v1/repositories/{repo_id}",
        json={"name": "Updated Repo"},
        headers=headers,
    )
    assert update_resp.status_code == 200
