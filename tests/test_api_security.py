"""HTTP security and error handling regression checks."""
import pytest
from fastapi.testclient import TestClient
from agents.api import app
from agents.llm_factory import LLMFactory

client = TestClient(app)


def test_unauthenticated_audit_logs_are_denied(monkeypatch):
    monkeypatch.delenv("AUDIT_LOG_READ_TOKEN", raising=False)
    assert client.get("/api/audit/logs").status_code == 403
    monkeypatch.setenv("AUDIT_LOG_READ_TOKEN", "test-token-do-not-use")
    assert client.get("/api/audit/logs").status_code == 403
    response = client.get("/api/audit/logs", headers={"X-Audit-Token": "test-token-do-not-use"})
    assert response.status_code == 200
    assert response.json()["verified"] is True


def test_identifier_pattern_is_validation_error_not_server_error():
    response = client.post("/api/audit", json={
        "task_id": "MRN-123456",
        "target_identifier": "TEST-TARGET",
        "primary_metric": 10,
    })
    assert response.status_code == 422
    assert "pattern" in response.json()["detail"]


def test_only_implemented_model_provider_is_accepted():
    with pytest.raises(ValueError, match="not implemented"):
        LLMFactory.create("ollama")
