"""Physical algebra checks for the idealized Majorana braid implementation."""
import math
import pytest
from majorana_braiding.braider import simulate_braids


def _close_pair(a, b):
    return all(math.isclose(x, y, abs_tol=1e-12) for x, y in zip(a, b))


def test_norm_preservation():
    for gates in ("", "12", "23", "12 23 12^-1 23^-1", "12 23 " * 100):
        assert math.isclose(simulate_braids(gates)["norm"], 1, abs_tol=1e-12)


def test_inverses_restore_initial_state():
    result = simulate_braids("12 23 23^-1 12^-1")
    assert _close_pair(result["amplitude0"], (1, 0))
    assert _close_pair(result["amplitude1"], (0, 0))


def test_nonabelian_exchange_and_braid_relation():
    left = simulate_braids("12 23 12")
    right = simulate_braids("23 12 23")
    assert _close_pair(left["amplitude0"], right["amplitude0"])
    assert _close_pair(left["amplitude1"], right["amplitude1"])
    a = simulate_braids("12 23")
    b = simulate_braids("23 12")
    assert not (_close_pair(a["amplitude0"], b["amplitude0"])
                and _close_pair(a["amplitude1"], b["amplitude1"]))


def test_invalid_sequences():
    with pytest.raises(ValueError, match="Unsupported"):
        simulate_braids("01")
    with pytest.raises(ValueError, match="512"):
        simulate_braids(["12"] * 513)
