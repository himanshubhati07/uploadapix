COMMIT_MESSAGE: remove integration delete endpoint and update env handling

## Features Added
- Removed the integration delete endpoint while keeping other integration APIs intact.

## Files Modified
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/app/routers/integrations.py - removed delete route handler
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/tests/test_integrations.py - removed delete test and updated name
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/app/database.py - load dotenv from new env file and rely on env database URL
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/app/core/security.py - load dotenv from new env file and read SECRET_KEY from env
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/tests/conftest.py - load dotenv from new env file
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/docker-compose.yml - updated database URL to resolved host
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/start.sh - use PORT env with 50619 default

## Files Added
- /home/ryzen/fast_api_generator_backend/outputs/299761e0-dfc4-4ccc-8fde-ee245d2f5212/.env_299761e0-dfc4-4ccc-8fde-ee245d2f5212 - runtime configuration

## Secrets Extracted
- SECRET_KEY -> written to .env_299761e0-dfc4-4ccc-8fde-ee245d2f5212

## DB URLs Resolved
- postgresql+asyncpg://myuser:mypassword@db:5432/gen_ae1525ed5f -> postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_51fe5c6eda

## Test Results Summary
- 9 PASSED, 0 FAILED, 0 SKIPPED
