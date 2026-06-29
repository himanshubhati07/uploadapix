# Auth endpoint tests.
import pytest
from tests.utils.factories import user_payload, login_payload


@pytest.mark.asyncio
async def test_register(client):
    payload = user_payload("-reg")
    resp = await client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == payload["email"]


@pytest.mark.asyncio
async def test_login_valid(client):
    payload = user_payload("-login")
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/login", json=login_payload(payload["email"]))
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_me_and_invalid_token(client):
    payload = user_payload("-me")
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json=login_payload(payload["email"]))
    token = login.json()["access_token"]

    profile = await client.get("/api/v1/auth/profile", headers={"Authorization": f"Bearer {token}"})
    assert profile.status_code == 200

    invalid = await client.get("/api/v1/auth/profile", headers={"Authorization": "Bearer badtoken"})
    assert invalid.status_code == 401
