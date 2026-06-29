# Server Logs [Iteration 0]

## Platform — OS + python version
- OS: linux
- Python: Python 3.11.2

## Database
- Client URL  : postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ae1525ed5f
- Fallback    : YES — substituted (original unreachable). DB name: gen_ae1525ed5f. Log in server_logs.md.
- Resolved URL: postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ae1525ed5f

## Test Runner — no live server needed
- pytest tests/ -v --tb=short  (tests use ASGI transport / TestClient — no HTTP server required)

## Files Generated / Modified
- /app/__init__.py — OK
- /app/database.py — OK
- /app/models.py — OK
- /app/schemas.py — OK
- /app/core/__init__.py — OK
- /app/core/security.py — OK
- /app/core/auth.py — OK
- /app/routers/__init__.py — OK
- /app/routers/auth.py — OK
- /app/routers/projects.py — OK
- /app/routers/analytics.py — OK
- /app/routers/integrations.py — OK
- /app/routers/repositories.py — OK
- /app/routers/deployments.py — OK
- /app/routers/services.py — OK
- /app/routers/issues.py — OK
- /app/routers/github.py — OK
- /app/routers/ws.py — OK
- /app/routers/catalog.py — OK
- /app/main.py — OK
- /seed.py — OK
- /requirements.txt — OK
- /.env_c880a487-d8cf-4cb1-82c9-3bfd459673d3 — OK
- /.env.example — OK
- /start.sh — OK
- /start.bat — OK
- /Dockerfile — OK
- /docker-compose.yml — OK
- /Makefile — OK
- /tests/__init__.py — OK
- /tests/conftest.py — OK
- /tests/test_auth.py — OK
- /tests/test_projects.py — OK
- /tests/test_integrations.py — OK
- /tests/test_repositories.py — OK
- /tests/test_deployments.py — OK
- /tests/test_services.py — OK
- /tests/test_issues.py — OK
- /tests/utils/__init__.py — OK
- /tests/utils/factories.py — OK
- /pytest.ini — OK
- /README.md — OK

## API Test Results

| Test Function | Endpoint | Status | Expected Code | Notes |
|---|---|---:|---:|---|
| test_register | POST /api/v1/auth/register | PASSED | 201 | User registration |
| test_login_valid | POST /api/v1/auth/login | PASSED | 200 | Valid credentials |
| test_me_and_invalid_token | GET /api/v1/auth/profile | PASSED | 200 | Authenticated profile |
| test_me_and_invalid_token | GET /api/v1/auth/profile (invalid token) | PASSED | 401 | Invalid credentials |
| test_create_get_actions_deployment | POST /api/v1/deployments | PASSED | 201 | Create deployment |
| test_create_get_actions_deployment | POST /api/v1/deployments/{id}/copy | PASSED | 200 | Copy deployment ID |
| test_create_get_actions_deployment | POST /api/v1/deployments/{id}/tunnel | PASSED | 200 | Open tunnel |
| test_create_list_get_update_delete_integration | POST /api/v1/integrations | PASSED | 201 | Create integration |
| test_create_list_get_update_delete_integration | GET /api/v1/integrations | PASSED | 200 | List integrations |
| test_create_list_get_update_delete_integration | GET /api/v1/integrations/{id} | PASSED | 200 | Get integration |
| test_create_list_get_update_delete_integration | PUT /api/v1/integrations/{id} | PASSED | 200 | Update integration |
| test_create_list_get_update_delete_integration | DELETE /api/v1/integrations/{id} | PASSED | 200 | Delete integration |
| test_list_and_resolve_issue | GET /api/v1/integration/issues | PASSED | 200 | List issues |
| test_list_and_resolve_issue | POST /api/v1/integration/issues/{id}/resolve | PASSED | 200 | Resolve issue |
| test_create_list_get_update_project | POST /api/v1/projects | PASSED | 201 | Create project |
| test_create_list_get_update_project | GET /api/v1/projects | PASSED | 200 | List projects |
| test_create_list_get_update_project | GET /api/v1/projects/{id} | PASSED | 200 | Get project |
| test_create_list_get_update_project | PUT /api/v1/projects/{id} | PASSED | 200 | Update project |
| test_create_get_update_repository | POST /api/v1/repositories | PASSED | 201 | Create repository |
| test_create_get_update_repository | GET /api/v1/repositories/{id} | PASSED | 200 | Get repository |
| test_create_get_update_repository | PUT /api/v1/repositories/{id} | PASSED | 200 | Update repository |
| test_create_start_stop_service | POST /api/v1/services | PASSED | 201 | Create service |
| test_create_start_stop_service | POST /api/v1/services/{id}/start | PASSED | 200 | Start service |
| test_create_start_stop_service | POST /api/v1/services/{id}/stop | PASSED | 200 | Stop service |

## Errors Fixed This Iteration
1. /app/models.py → typing error for forward references → added future annotations and Optional relationships.
2. /tests/conftest.py → missing test DB and DSN issues → created test DB with asyncpg and fixed DSN rendering.
3. /app/schemas.py → UUID response validation errors → converted UUID fields to UUID types.
4. /tests/utils/factories.py → duplicate user emails → added random suffix.
5. /tests/conftest.py → seed data uniqueness violations → randomized seed values and guarded rollback.
6. /requirements.txt → missing email-validator for EmailStr → added dependency.

## Still Failing
