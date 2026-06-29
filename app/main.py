# FastAPI application entrypoint.
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, projects, analytics, integrations, repositories, deployments, services, issues, github, ws, catalog

load_dotenv('.env_c880a487-d8cf-4cb1-82c9-3bfd459673d3', override=True)

app = FastAPI(title="figma new", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(projects.router, prefix=API_PREFIX)
app.include_router(analytics.router, prefix=API_PREFIX)
app.include_router(integrations.router, prefix=API_PREFIX)
app.include_router(integrations.aux_router, prefix=API_PREFIX)
app.include_router(repositories.router, prefix=API_PREFIX)
app.include_router(repositories.analysis_router, prefix=API_PREFIX)
app.include_router(deployments.router, prefix=API_PREFIX)
app.include_router(services.router, prefix=API_PREFIX)
app.include_router(services.log_router, prefix=API_PREFIX)
app.include_router(services.action_router, prefix=API_PREFIX)
app.include_router(issues.router, prefix=API_PREFIX)
app.include_router(github.router, prefix=API_PREFIX)
app.include_router(github.user_router, prefix=API_PREFIX)
app.include_router(catalog.router, prefix=API_PREFIX)
app.include_router(ws.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
