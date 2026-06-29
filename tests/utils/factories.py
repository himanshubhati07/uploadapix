# Test payload factories.
from uuid import uuid4


def user_payload(email_suffix: str = ""):
    unique = uuid4().hex[:8]
    return {
        "full_name": "Test User",
        "email": f"user{email_suffix}-{unique}@example.com",
        "password": "Password1",
        "remember_me": False,
    }


def login_payload(email: str):
    return {"email": email, "password": "Password1"}


def project_payload():
    return {"name": f"Project {uuid4().hex[:6]}", "status": "in_progress"}


def integration_payload():
    return {
        "name": f"Integration {uuid4().hex[:6]}",
        "status": "pending",
        "frontend_repo_url": "https://github.com/example/frontend",
        "backend_repo_url": "https://github.com/example/backend",
    }


def repository_payload(repo_type: str = "frontend"):
    return {
        "name": f"Repo {uuid4().hex[:6]}",
        "url": f"https://github.com/example/{uuid4().hex[:6]}",
        "repo_type": repo_type,
    }


def deployment_payload():
    dep_id = f"dep-{uuid4().hex[:6]}"
    return {"deployment_id": dep_id, "name": f"Deployment {dep_id}", "status": "pending"}


def service_payload():
    return {
        "name": f"Service {uuid4().hex[:6]}",
        "service_type": "frontend",
        "url": f"https://service-{uuid4().hex[:6]}.example.com",
        "status": "stopped",
    }


def issue_payload():
    return {
        "title": "Issue title",
        "description": "Issue description",
        "issue_type": "critical",
        "affected_component": "backend",
    }
