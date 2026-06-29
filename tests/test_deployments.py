# Deployment endpoint tests.
import pytest
from tests.utils.factories import user_payload, login_payload, deployment_payload


async def get_token(client):
    payload = user_payload("-deploy")
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json=login_payload(payload["email"]))
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_create_get_actions_deployment(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = await client.post("/api/v1/deployments", json=deployment_payload(), headers=headers)
    assert create_resp.status_code == 201
    deployment_id = create_resp.json()["id"]

    get_resp = await client.get(f"/api/v1/deployments/{deployment_id}", headers=headers)
    assert get_resp.status_code == 200

    copy_resp = await client.post(f"/api/v1/deployments/{deployment_id}/copy", headers=headers)
    assert copy_resp.status_code == 200

    tunnel_resp = await client.post(f"/api/v1/deployments/{deployment_id}/tunnel", headers=headers)
    assert tunnel_resp.status_code == 200
