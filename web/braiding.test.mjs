import test from 'node:test';
import assert from 'node:assert/strict';
import { parseSequence, simulateBraids, evaluateThresholdAudit } from './braiding.mjs';

const near = (a, b, eps = 1e-12) => Math.abs(a - b) < eps;
const nearComplex = (a, b) => a.every((v, i) => near(v, b[i]));

test('identity and exchanges preserve probability', () => {
  for (const input of ['', '12', '23', '12 23 12^-1 23^-1', '12 23 '.repeat(100)]) {
    const state = simulateBraids(input);
    assert.ok(near(state.norm, 1), input);
  }
  assert.ok(near(simulateBraids('12').probability0, 1));
  assert.ok(near(simulateBraids('23').probability0, 0.5));
});

test('inverse exchanges undo the forward operation', () => {
  const state = simulateBraids('12 23 23^-1 12^-1');
  assert.ok(nearComplex(state.amplitude0, [1, 0]));
  assert.ok(nearComplex(state.amplitude1, [0, 0]));
});

test('braid relation holds and generators do not commute', () => {
  const lhs = simulateBraids('12 23 12');
  const rhs = simulateBraids('23 12 23');
  assert.ok(nearComplex(lhs.amplitude0, rhs.amplitude0));
  assert.ok(nearComplex(lhs.amplitude1, rhs.amplitude1));
  const ab = simulateBraids('12 23');
  const ba = simulateBraids('23 12');
  assert.equal(nearComplex(ab.amplitude0, ba.amplitude0)
    && nearComplex(ab.amplitude1, ba.amplitude1), false);
});

test('reject invalid and excessive exchange labels', () => {
  assert.deepEqual(parseSequence('12, 23 12^-1'), ['12', '23', '12^-1']);
  assert.throws(() => simulateBraids('01'), /Unsupported/);
  assert.throws(() => simulateBraids('12 '.repeat(513)), /512/);
});

test('threshold demo matches the configured legacy rules', () => {
  const base = { task_id: 'T1', target_identifier: 'X1', primary_metric: 10,
    secondary_metric: 5, status_descriptor: 'NOMINAL', is_critical_flag: false };
  assert.equal(evaluateThresholdAudit(base).overall_urgency, 'ROUTINE');
  assert.equal(evaluateThresholdAudit({...base, primary_metric: 26}).overall_urgency, 'ELEVATED_RISK');
  assert.equal(evaluateThresholdAudit({...base, is_critical_flag: true}).overall_urgency, 'CRITICAL_STAT_PANIC');
  assert.throws(() => evaluateThresholdAudit({...base, primary_metric: Infinity}), /finite/);
});
