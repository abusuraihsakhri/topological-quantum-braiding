/** Idealized three-Majorana braid representation on a two-state Hilbert space. */
const S = Math.SQRT1_2;
const multiply = ([ar, ai], [br, bi]) => [ar * br - ai * bi, ar * bi + ai * br];
const add = ([ar, ai], [br, bi]) => [ar + br, ai + bi];
const scale = ([re, im], value) => [re * value, im * value];
const validGates = new Set(['12', '23', '12^-1', '23^-1']);

export function parseSequence(input) {
  if (typeof input !== 'string') throw new TypeError('Sequence must be text');
  const gates = input.trim().split(/[\s,]+/).filter(Boolean);
  if (gates.length > 512) throw new RangeError('Use at most 512 exchanges');
  for (const gate of gates) {
    if (!validGates.has(gate)) throw new Error('Unsupported exchange: ' + gate);
  }
  return gates;
}

export function simulateBraids(sequence) {
  const gates = Array.isArray(sequence) ? sequence : parseSequence(sequence);
  if (gates.length > 512 || gates.some(gate => !validGates.has(gate))) {
    throw new Error('Invalid braid sequence');
  }
  let a = [1, 0];
  let b = [0, 0];
  for (const gate of gates) {
    const sign = gate.endsWith('^-1') ? -1 : 1;
    if (gate.startsWith('12')) {
      a = multiply([S, sign * S], a);
      b = multiply([S, -sign * S], b);
    } else {
      const nextA = scale(add(a, multiply([0, sign], b)), S);
      const nextB = scale(add(multiply([0, sign], a), b), S);
      a = nextA;
      b = nextB;
    }
  }
  const probability = ([real, imaginary]) => real ** 2 + imaginary ** 2;
  const p0 = probability(a);
  const p1 = probability(b);
  return { sequence: [...gates], amplitude0: a, amplitude1: b,
    probability0: p0, probability1: p1, norm: p0 + p1 };
}

/** Mirrors the legacy rule-based workers; not a physical braiding calculation. */
export function evaluateThresholdAudit(payload) {
  const taskId = String(payload.task_id ?? '').trim();
  const targetId = String(payload.target_identifier ?? '').trim();
  const primary = payload.primary_metric;
  const secondary = payload.secondary_metric;
  const descriptor = String(payload.status_descriptor ?? '').trim();
  if (!taskId || !targetId) throw new Error('Task and target identifiers are required');
  if (!Number.isFinite(primary) || !Number.isFinite(secondary)) {
    throw new Error('Both metrics must be finite numbers');
  }
  const alerts = [];
  if (primary > 25) alerts.push({ worker: 'InvariantQCWorker', urgency: 'ELEVATED_RISK',
    summary: 'Primary metric exceeds illustrative threshold (25)' });
  if (payload.is_critical_flag || secondary > 12) {
    alerts.push({ worker: 'SafetyEscalationWorker',
      urgency: payload.is_critical_flag ? 'CRITICAL_STAT_PANIC' : 'ELEVATED_RISK',
      summary: 'Critical flag or secondary metric exceeds illustrative threshold (12)' });
  }
  if (['DISCORDANT', 'ANOMALY', 'MUTANT', 'VIOLATION', 'FAIL', 'REJECT']
    .some(word => descriptor.toUpperCase().includes(word))) {
    alerts.push({ worker: 'ProtocolConformanceWorker', urgency: 'ELEVATED_RISK',
      summary: 'Descriptor matches a configured anomaly keyword' });
  }
  const overall = alerts.some(x => x.urgency === 'CRITICAL_STAT_PANIC')
    ? 'CRITICAL_STAT_PANIC' : alerts.length ? 'ELEVATED_RISK' : 'ROUTINE';
  return { task_id: taskId, target_identifier: targetId, overall_urgency: overall,
    integrity_status: overall === 'CRITICAL_STAT_PANIC' ? 'RECALIBRATION_REQUIRED'
      : overall === 'ELEVATED_RISK' ? 'DISCORDANT_ANOMALY' : 'VALIDATED_OPTIMAL',
    total_alerts: alerts.length, critical_alerts_count:
      alerts.filter(x => x.urgency === 'CRITICAL_STAT_PANIC').length,
    alerts, note: 'Local deterministic demonstration; no cryptographic audit trail or standards validation.' };
}
