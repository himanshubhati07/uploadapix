# Integration endpoint tests.
import pytest
from tests.utils.factories import user_payload, login_payload, integration_payload


async def get_token(client):
    payload = user_payload("-integrations")
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json=login_payload(payload["email"]))
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_create_list_get_update_delete_integration(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post("/api/v1/integrations", json=integration_payload(), headers=headers)
    assert create_resp.status_code == 201
    integration_id = create_resp.json()["id"]

    list_resp = await client.get("/api/v1/integrations", headers=headers)
    assert list_resp.status_code == 200

    get_resp = await client.get(f"/api/v1/integrations/{integration_id}", headers=headers)
    assert get_resp.status_code == 200

    update_resp = await client.put(
        f"/api/v1/integrations/{integration_id}",
        json={"name": "Updated Integration"},
        headers=headers,
    )
    assert update_resp.status_code == 200

    delete_resp = await client.delete(f"/api/v1/integrations/{integration_id}", headers=headers)
    assert delete_resp.status_code == 200
