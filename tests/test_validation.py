"""
Input Validation & Security Tests for Topological Quantum Braiding.
"""
import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.models import SystemTaskPayload, UrgencyLevel
from agents.base import PHIGuard, SecurityException, AuditTrail


class TestInputValidation:
    """Tests for metric value and identifier validation."""

    def test_reject_nan_primary_metric(self):
        with pytest.raises(ValueError, match="finite"):
            SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=math.nan)

    def test_reject_inf_primary_metric(self):
        with pytest.raises(ValueError, match="finite"):
            SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=math.inf)

    def test_reject_neg_inf_secondary_metric(self):
        with pytest.raises(ValueError, match="finite"):
            SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=10.0, secondary_metric=-math.inf)

    def test_reject_blank_task_id(self):
        with pytest.raises(ValueError):
            SystemTaskPayload(task_id="   ", target_identifier="KEY-01", primary_metric=10.0)

    def test_reject_blank_target_identifier(self):
        with pytest.raises(ValueError):
            SystemTaskPayload(task_id="T1", target_identifier="", primary_metric=10.0)

    def test_accept_valid_payload(self):
        p = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=10.0, secondary_metric=5.0)
        assert p.task_id == "T1"
        assert p.primary_metric == 10.0

    def test_accept_zero_metrics(self):
        p = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=0.0, secondary_metric=0.0)
        assert p.primary_metric == 0.0

    def test_accept_negative_metrics(self):
        """Negative values are physically valid for some measurements."""
        p = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=-5.0, secondary_metric=-2.0)
        assert p.primary_metric == -5.0

    def test_whitespace_stripped_from_identifiers(self):
        p = SystemTaskPayload(task_id="  T1  ", target_identifier="  KEY-01  ", primary_metric=10.0)
        assert p.task_id == "T1"
        assert p.target_identifier == "KEY-01"


class TestPHIGuardEdgeCases:
    """Additional PHI guard tests."""

    def test_clean_text_passes(self):
        PHIGuard.assert_no_phi("Analytical specimen KEY-001 optimal")

    def test_reject_mrn_pattern(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Patient MRN-12345678")

    def test_reject_ssn_pattern(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("SSN: 123-45-6789")

    def test_reject_email_pattern(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Contact patient@hospital.org for results")

    def test_reject_phone_pattern(self):
        with pytest.raises(SecurityException):
            PHIGuard.assert_no_phi("Call 555-123-4567 for critical results")

    def test_empty_string_passes(self):
        PHIGuard.assert_no_phi("")

    def test_none_handled_gracefully(self):
        PHIGuard.assert_no_phi(None)

    def test_redact_phi_replaces_sensitive_data(self):
        result = PHIGuard.redact_phi("Patient MRN-12345 has SSN 123-45-6789")
        assert "MRN" not in result or "REDACTED" in result
        assert "123-45-6789" not in result


class TestAuditTrailIntegrity:
    """Tests for HMAC-SHA256 audit trail."""

    def test_audit_trail_chains_correctly(self):
        trail = AuditTrail(secret_key="test-key-123")
        trail.log("actor1", "tier1", "EVENT_A", {"data": "value1"})
        trail.log("actor2", "tier2", "EVENT_B", {"data": "value2"})
        assert trail.verify_integrity() is True
        assert len(trail.get_trail()) == 2

    def test_audit_trail_detects_tampering(self):
        trail = AuditTrail(secret_key="test-key-123")
        trail.log("actor1", "tier1", "EVENT_A", {"data": "value1"})
        trail.log("actor2", "tier2", "EVENT_B", {"data": "value2"})
        # Tamper with the first entry's hash
        trail.logs[0]["current_hash"] = "TAMPERED_HASH"
        assert trail.verify_integrity() is False

    def test_audit_trail_rejects_phi_in_details(self):
        trail = AuditTrail(secret_key="test-key-123")
        with pytest.raises(SecurityException):
            trail.log("actor1", "tier1", "EVENT_A", {"patient": "MRN-12345"})

    def test_audit_trail_empty_is_valid(self):
        trail = AuditTrail(secret_key="test-key-123")
        assert trail.verify_integrity() is True
        assert len(trail.get_trail()) == 0
