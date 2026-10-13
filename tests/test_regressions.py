"""Regression tests for audit integrity and boolean CSV deserialization."""
import csv
import pytest
from agents.base import AuditTrail
from cli import main as primary_main
from majorana_braiding.cli import main as legacy_main


@pytest.mark.parametrize("field", ["event_type", "payload_hash", "actor", "current_hash"])
def test_audit_detects_single_entry_tampering(field):
    ledger = AuditTrail(secret_key="test-only-secret")
    ledger.log("unit", "test", "DONE", {"ok": True})
    ledger.logs[0][field] = "tampered"
    assert not ledger.verify_integrity()


def test_ledger_returns_defensive_copy():
    ledger = AuditTrail(secret_key="test-only-secret")
    ledger.log("unit", "test", "DONE", {"ok": True})
    snapshot = ledger.get_trail()
    snapshot[0]["event_type"] = "tampered"
    assert ledger.verify_integrity()


@pytest.mark.parametrize("cli", [primary_main, legacy_main])
def test_csv_false_and_true_values(cli, tmp_path):
    source = tmp_path / "tasks.csv"
    output = tmp_path / "results.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\\n"
        "NO,X1,2,2,False,NOMINAL\\n"
        "YES,X2,2,2,true,NOMINAL\\n",
        encoding="utf-8",
    )
    assert cli(["batch", "-i", str(source), "-o", str(output)]) == 0
    with output.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    field = "overall_urgency" if cli is primary_main else "overall_status"
    assert rows[0][field] in ("ROUTINE", "NOMINAL_OPTIMAL")
    assert rows[1][field] in ("CRITICAL_STAT_PANIC", "CRITICAL_INTERVENTION_REQUIRED")


@pytest.mark.parametrize("cli", [primary_main, legacy_main])
def test_csv_rejects_unknown_bool(cli, tmp_path):
    source = tmp_path / "tasks.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag\\n"
        "X,Y,2,2,perhaps\\n", encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Invalid boolean"):
        cli(["batch", "-i", str(source), "-o", str(tmp_path / "out.csv")])
