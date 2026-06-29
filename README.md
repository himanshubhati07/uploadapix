# figma new FastAPI Backend

## Overview
Production-ready FastAPI backend implementing authentication (JWT), project/integration management, repository analysis, GitHub integration, deployments, services monitoring, issues tracking, and analytics. All private APIs are protected by JWT.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables
Create `.env_c880a487-d8cf-4cb1-82c9-3bfd459673d3`:
```
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ae1525ed5f
SECRET_KEY=super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PORT=48369
```

## Run
```bash
bash start.sh
```

## Tests
```bash
pytest tests/ -v --tb=short
```

## API Sample Responses
- **Login** `POST /api/v1/auth/login`
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 1800
}
```
- **Invalid Token** (401)
```json
{
  "detail": "Your session has expired or the authentication token is invalid. Please log in again."
}
```

## Key Endpoints
- Auth: `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/logout`, `/api/v1/auth/refresh`, `/api/v1/auth/profile`, `/api/v1/auth/validate-token`, `/api/v1/auth/google`
- Projects: `/api/v1/projects`, `/api/v1/projects/{id}`, `/api/v1/projects/{id}/analytics`, `/api/v1/projects/{id}/history`, `/api/v1/projects/overview`, `/api/v1/projects/history`
- Integrations: `/api/v1/integrations`, `/api/v1/integrations/{id}`, `/api/v1/integrations/{id}/analyze`, `/api/v1/integrations/{id}/launch`, `/api/v1/integration/status/{analysis_id}`, `/api/v1/integration/stop`
- Repositories: `/api/v1/repositories`, `/api/v1/repositories/{id}`, `/api/v1/repositories/{id}/compatibility_check`, `/api/v1/repositories/{id}/dependency_analysis`
- GitHub: `/api/v1/integrations/github`, `/api/v1/integrations/github/status`, `/api/v1/integrations/github (DELETE)`, `/api/v1/user/github-access`
- Deployments: `/api/v1/deployments`, `/api/v1/deployments/{id}`, `/api/v1/deployments/{id}/copy`, `/api/v1/deployments/{id}/tunnel`
- Services: `/api/v1/services`, `/api/v1/services/{id}/start`, `/api/v1/services/{id}/stop`, `/api/v1/logs/{service_id}`, `/api/v1/actions/history`
- WebSocket: `/ws/ping`

## Docker
```bash
docker compose up --build
```

## Project Tree
```
app/
  core/
  routers/
  database.py
  models.py
  schemas.py
  main.py
seed.py
start.sh
start.bat
```
