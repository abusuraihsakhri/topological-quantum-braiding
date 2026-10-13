"""
FastAPI REST API Server for Topological Quantum Braiding.
"""
import os
import hmac
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Topological Quantum Braiding API",
    description="Enterprise Distributed Component Platform (Post-Quantum Cryptography & Hardware Security)",
    version="3.0.0-ENTERPRISE",
)


@app.exception_handler(SecurityException)
async def handle_sensitive_input(request, exc: SecurityException):
    return JSONResponse(
        status_code=422,
        content={"detail": "Input contains a pattern resembling a sensitive identifier"},
    )


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "topological-quantum-braiding", "domain": "Post-Quantum Cryptography & Hardware Security", "standard": "NIST FIPS 203/204/205 / ISO/IEC 17825 Standards", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    dossier = supervisor.process_task(payload)
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    return {"response": supervisor.query_supervisory_chat(req.query)}


@app.get("/api/audit/logs")
def api_audit_logs(x_audit_token: str = Header(default="")):
    """Deny audit-log reads unless an explicit read token is configured."""
    expected = os.getenv("AUDIT_LOG_READ_TOKEN", "")
    if not expected or not hmac.compare_digest(x_audit_token, expected):
        raise HTTPException(status_code=403, detail="Audit-log access is disabled or unauthorized")
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
