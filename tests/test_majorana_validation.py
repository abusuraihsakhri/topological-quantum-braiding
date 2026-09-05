"""
Input Validation Tests for Majorana Zero Mode (MZM) Non-Abelian Anyon Braiding Simulator.
"""
import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from majorana_braiding.models import FrontierPayload, ExecutionStatus


class TestFrontierPayloadValidation:
    """Tests for FrontierPayload input validation."""

    def test_reject_nan_primary_metric(self):
        with pytest.raises(ValueError, match="finite"):
            FrontierPayload(task_id="T1", target_identifier="KEY-01", primary_metric=math.nan,
                           secondary_metric=5.0, status_descriptor="NOMINAL")

    def test_reject_inf_secondary_metric(self):
        with pytest.raises(ValueError, match="finite"):
            FrontierPayload(task_id="T1", target_identifier="KEY-01", primary_metric=10.0,
                           secondary_metric=math.inf, status_descriptor="NOMINAL")

    def test_reject_blank_task_id(self):
        with pytest.raises(ValueError, match="blank"):
            FrontierPayload(task_id="", target_identifier="KEY-01", primary_metric=10.0,
                           secondary_metric=5.0, status_descriptor="NOMINAL")

    def test_reject_blank_target_identifier(self):
        with pytest.raises(ValueError, match="blank"):
            FrontierPayload(task_id="T1", target_identifier="   ", primary_metric=10.0,
                           secondary_metric=5.0, status_descriptor="NOMINAL")

    def test_accept_valid_payload(self):
        p = FrontierPayload(task_id="T1", target_identifier="KEY-01", primary_metric=10.0,
                           secondary_metric=5.0, status_descriptor="NOMINAL")
        assert p.task_id == "T1"
        assert p.primary_metric == 10.0

    def test_accept_negative_metrics(self):
        p = FrontierPayload(task_id="T1", target_identifier="KEY-01", primary_metric=-5.0,
                           secondary_metric=-2.0, status_descriptor="NOMINAL")
        assert p.primary_metric == -5.0


class TestFrontierEngine:
    """Tests for FrontierDomainEngine."""

    def test_primary_boundary_detection(self):
        from majorana_braiding.engine import FrontierDomainEngine
        result = FrontierDomainEngine.evaluate_primary_parameter(30.0)
        assert result is not None
        assert "exceeds" in result["details"]

    def test_primary_within_bounds(self):
        from majorana_braiding.engine import FrontierDomainEngine
        result = FrontierDomainEngine.evaluate_primary_parameter(10.0)
        assert result is None

    def test_secondary_critical_flag(self):
        from majorana_braiding.engine import FrontierDomainEngine
        result = FrontierDomainEngine.evaluate_secondary_kinetics(5.0, is_critical=True)
        assert result is not None

    def test_specification_conformance_discordant(self):
        from majorana_braiding.engine import FrontierDomainEngine
        result = FrontierDomainEngine.audit_specification_conformance("DISCORDANT_ANOMALY", {})
        assert result is not None

    def test_specification_conformance_nominal(self):
        from majorana_braiding.engine import FrontierDomainEngine
        result = FrontierDomainEngine.audit_specification_conformance("NOMINAL", {})
        assert result is None
