# Issue endpoint tests.
import pytest
from tests.utils.factories import user_payload, login_payload


async def get_token(client):
    payload = user_payload("-issues")
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json=login_payload(payload["email"]))
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_list_and_resolve_issue(client, seed_data):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    list_resp = await client.get("/api/v1/integration/issues", headers=headers)
    assert list_resp.status_code == 200

    issue_id = seed_data["issue"].id
    resolve_resp = await client.post(f"/api/v1/integration/issues/{issue_id}/resolve", headers=headers)
    assert resolve_resp.status_code == 200
