# Service endpoint tests.
import pytest
from tests.utils.factories import user_payload, login_payload, service_payload


async def get_token(client):
    payload = user_payload("-services")
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json=login_payload(payload["email"]))
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_create_start_stop_service(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post("/api/v1/services", json=service_payload(), headers=headers)
    assert create_resp.status_code == 201
    service_id = create_resp.json()["id"]

    start_resp = await client.post(f"/api/v1/services/{service_id}/start", headers=headers)
    assert start_resp.status_code == 200

    stop_resp = await client.post(f"/api/v1/services/{service_id}/stop", headers=headers)
    assert stop_resp.status_code == 200
