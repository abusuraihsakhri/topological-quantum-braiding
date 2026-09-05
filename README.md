# Topological Quantum Braiding

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Topological Quantum Braiding is an enterprise-grade distributed component platform that simulates Majorana Zero Mode (MZM) non-Abelian anyon braiding for topological quantum computing research. It provides:

- **Multi-Agent Evaluation Pipeline**: Three specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) analyze task payloads and generate consensus dossiers.
- **Zero-PHI Outbound Interceptor**: Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers from leaving the system.
- **Tamper-Evident HMAC-SHA256 Audit Trail**: Chained, cryptographically signed logs for every evaluation and state transition.
- **FastAPI REST API**: OpenAPI 3.1 endpoints for task evaluation, chat, and audit log retrieval.
- **Prometheus Telemetry**: Operational metrics exposed at `/metrics`.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization (ROUTINE, ELEVATED_RISK, CRITICAL_STAT_PANIC) with automated action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking, NaN/Infinity rejection, and anomaly detection.
- **Active Learning Bayesian Calibration**: Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.

---

## 💻 CLI Quickstart & Usage

### Installation

```bash
pip install -e .
```

### 1. Run Single Task Evaluation (Audit)

```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Supervisory Chat Query

```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records

```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity

```bash
python cli.py verify-audit
```

### 5. Launch FastAPI REST Server

```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference

| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task identifier | `TASK-2026-001` |
| `--target` | Target entity or key | `KEY-TARGET-01` |
| `--primary` | Primary measurement value (float) | `28.5` |
| `--secondary` | Secondary metric value (float) | `14.2` |
| `--critical` | Flag for critical/emergency status | `False` |
| `--status` | Status descriptor (NOMINAL, DISCORDANT, etc.) | `DISCORDANT` |

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task identifier | Required |
| `target_identifier` | Target entity or key | Required |
| `primary_metric` | Primary measurement value | Required |
| `secondary_metric` | Secondary metric value | Optional (default: 0.0) |
| `is_critical_flag` | Emergency escalation flag | Optional (default: False) |
| `status_descriptor` | Status code or phenotype | Optional (default: NOMINAL) |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Configuration

Set the `AUDIT_SECRET_KEY` environment variable in production to ensure cryptographic audit trail integrity:

```bash
# Linux/macOS
export AUDIT_SECRET_KEY="your-secure-random-key-here"

# Windows
set AUDIT_SECRET_KEY=your-secure-random-key-here
```

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 1000
```

### Test Coverage

- **PHI Guard Enforcement**: Validates zero-PHI outbound interceptor blocks sensitive identifiers.
- **Specialized Workers**: Tests InvariantQCWorker, SafetyEscalationWorker, and ProtocolConformanceWorker alert generation.
- **Supervisor Consensus**: Verifies multi-agent consensus and HMAC audit trail integrity.
- **Enrichment Suite**: Tests Majorana Zero Mode braiding and Topological Surface Code engines.
- **Input Validation**: Validates NaN/Infinity rejection and identifier format enforcement.

---

## 🐳 Container Deployment

```bash
docker build -t topological-quantum-braiding .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secure-key topological-quantum-braiding
```

Or using Docker Compose:

```bash
AUDIT_SECRET_KEY=your-secure-key docker compose up
```

---

## 📁 Project Structure

```
topological-quantum-braiding/
├── agents/                      # Enterprise supervisor system
│   ├── __init__.py
│   ├── api.py                   # FastAPI REST endpoints
│   ├── base.py                  # PHI guard, HMAC audit trail
│   ├── learning.py              # Bayesian calibration engine
│   ├── llm_factory.py           # LLM provider factory
│   ├── metrics.py               # Prometheus metrics collector
│   ├── models.py                # Pydantic schemas
│   ├── streamer.py              # WebSocket telemetry
│   ├── supervisor.py            # Master coordinator
│   └── workers.py               # Specialized evaluation workers
├── majorana_braiding/           # Frontier domain simulator
│   ├── __init__.py
│   ├── agents.py                # Majorana braiding agents
│   ├── cli.py                   # CLI for frontier simulator
│   ├── engine.py                # Core algorithmic engine
│   ├── models.py                # Data models
│   └── server.py                # FastAPI server factory
├── tests/                       # Pytest test suite
│   ├── test_enrichment.py
│   ├── test_majorana_braiding.py
│   └── test_topological_quantum_braiding.py
├── web/                         # Operations console (HTML)
├── cli.py                       # Main CLI entry point
├── simulator.py                 # High-throughput simulation
├── enrichment.py                # Enrichment feature modules
├── pyproject.toml               # Project configuration
├── Dockerfile                   # Container build
├── docker-compose.yml           # Container orchestration
└── .github/workflows/ci.yml     # CI/CD pipeline
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
