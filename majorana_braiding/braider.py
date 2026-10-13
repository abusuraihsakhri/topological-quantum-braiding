"""Idealized non-Abelian Majorana exchange operators in a two-state representation.

The model applies exp(pi/4 * gamma_i gamma_j) with gamma_1, gamma_2,
gamma_3 represented by the Pauli matrices. It does not simulate a physical
T-junction Hamiltonian, adiabatic timing, decoherence, or device hardware.
"""
from __future__ import annotations

import math
from typing import Iterable, Union

_S = math.sqrt(0.5)
_ALLOWED = {"12", "23", "12^-1", "23^-1"}


def simulate_braids(sequence: Union[str, Iterable[str]]) -> dict:
    """Apply exchanges left to right to |0>; return JSON-safe amplitudes.

    Supported generator labels are 12, 23, 12^-1, and 23^-1.
    """
    if isinstance(sequence, str):
        gates = sequence.replace(",", " ").split()
    else:
        gates = list(sequence)

    if len(gates) > 512:
        raise ValueError("Use at most 512 exchanges")
    for gate in gates:
        if not isinstance(gate, str) or gate not in _ALLOWED:
            raise ValueError(f"Unsupported exchange: {gate!r}")

    a, b = complex(1), complex(0)
    for gate in gates:
        sign = -1 if gate.endswith("^-1") else 1
        if gate.startswith("12"):
            a, b = complex(_S, sign * _S) * a, complex(_S, -sign * _S) * b
        else:
            a, b = _S * (a + sign * 1j * b), _S * (sign * 1j * a + b)

    p0, p1 = abs(a) ** 2, abs(b) ** 2
    return {
        "sequence": gates,
        "amplitude0": [a.real, a.imag],
        "amplitude1": [b.real, b.imag],
        "probability0": p0,
        "probability1": p1,
        "norm": p0 + p1,
    }
