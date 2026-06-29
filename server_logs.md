# Server Logs [Iteration 0]

## Platform - OS + python version
- OS: linux
- Python: 3.11.2

## Database
- Original URLs : postgresql+asyncpg://myuser:mypassword@db:5432/gen_ae1525ed5f; postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ae1525ed5f
- Resolved URLs : postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_51fe5c6eda; postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ae1525ed5f
- Env file      : .env_299761e0-dfc4-4ccc-8fde-ee245d2f5212

## Start Script - which script was used
- start.sh (PORT=50619)

## Files Generated / Modified
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/app/routers/integrations.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/tests/test_integrations.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/app/database.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/app/core/security.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/tests/conftest.py - OK
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/docker-compose.yml - OK
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/start.sh - OK
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/.env_299761e0-dfc4-4ccc-8fde-ee245d2f5212 - OK

## API Test Results

| Method | Path | Status | HTTP Code | Notes |
|---|---|---:|---:|---|
| GET | /health | PASSED | 200 | Health check OK |
| POST | /api/v1/auth/register | PASSED | 201 | Registration OK |
| POST | /api/v1/auth/login | PASSED | 200 | Login OK |
| GET | /api/v1/auth/profile | PASSED | 200 | Profile OK |
| GET | /api/v1/auth/profile | PASSED | 401 | Invalid token |
| POST | /api/v1/deployments | PASSED | 201 | Create deployment |
| GET | /api/v1/deployments/{id} | PASSED | 200 | Get deployment |
| POST | /api/v1/deployments/{id}/copy | PASSED | 200 | Copy path |
| POST | /api/v1/deployments/{id}/tunnel | PASSED | 200 | Open tunnel |
| POST | /api/v1/integrations | PASSED | 201 | Create integration |
| GET | /api/v1/integrations | PASSED | 200 | List integrations |
| GET | /api/v1/integrations/{id} | PASSED | 200 | Get integration |
| PUT | /api/v1/integrations/{id} | PASSED | 200 | Update integration |
| GET | /api/v1/integration/issues | PASSED | 200 | List issues |
| POST | /api/v1/integration/issues/{id}/resolve | PASSED | 200 | Resolve issue |
| POST | /api/v1/projects | PASSED | 201 | Create project |
| GET | /api/v1/projects | PASSED | 200 | List projects |
| GET | /api/v1/projects/{id} | PASSED | 200 | Get project |
| PUT | /api/v1/projects/{id} | PASSED | 200 | Update project |
| POST | /api/v1/repositories | PASSED | 201 | Create repository |
| GET | /api/v1/repositories/{id} | PASSED | 200 | Get repository |
| PUT | /api/v1/repositories/{id} | PASSED | 200 | Update repository |
| POST | /api/v1/services | PASSED | 201 | Create service |
| POST | /api/v1/services/{id}/start | PASSED | 200 | Start service |
| POST | /api/v1/services/{id}/stop | PASSED | 200 | Stop service |

## Errors Fixed This Iteration
1. start.sh -> hardcoded port 48369 caused bind failure -> switched to use PORT env with 50619 default

