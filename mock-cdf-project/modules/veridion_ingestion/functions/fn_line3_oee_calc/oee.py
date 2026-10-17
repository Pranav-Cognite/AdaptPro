"""Hourly OEE for a production line, per the Line 3 OEE Calculation SOP (rev B).

Pure functions, no CDF calls, so the same logic runs inside the CDF Function
(handler.py) and in the fixture generator (mock-cdf-project/fixtures/generate_datapoints.py).

OEE = Availability x Performance x Quality, per clock hour (UTC):

  planned time  = 60 min, minus planned downtime if `exclude_planned` (SOP rev B: changeovers
                  and planned maintenance are not a loss)
  run time      = 60 min minus the union of all downtime windows (overlaps are merged, so a
                  stop logged twice in SAP is counted once)
  Availability  = run time / planned time
  Performance   = produced kg / (ideal rate x run time)       (capped at 100 %)
  Quality       = good kg / (good kg + reject kg)              (MES counts)

Known behaviours that are deliberate, not bugs:
  * An activity with no end time (an SAP notification nobody closed) is ignored. The lost
    output then shows up as Performance loss, not Availability loss.
  * A clock hour with any missing process datapoint yields no OEE (a gap, not a zero).
  * Micro-stops that were never logged in SAP are Performance loss by construction.
"""
from datetime import datetime, timedelta, timezone

UTC = timezone.utc
BUCKET_MIN = 15
IDEAL_RATE_SOP_REV_B = 3800.0     # kg/h, demonstrated rate agreed under MOC-2025-014
IDEAL_RATE_MES_LEGACY = 4200.0    # kg/h, old nameplate figure still used by the legacy MES report


def _overlap_min(a0, a1, b0, b1):
    lo, hi = max(a0, b0), min(a1, b1)
    return max(0.0, (hi - lo).total_seconds() / 60.0)


def _merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def _clip(intervals, h0, h1):
    return [(max(s, h0), min(e, h1)) for s, e in intervals if min(e, h1) > max(s, h0)]


def _total_min(intervals):
    return sum((e - s).total_seconds() / 60.0 for s, e in intervals)


def compute_hour(h0, activities, rates, good_kg, reject_kg,
                 ideal_rate=IDEAL_RATE_SOP_REV_B, exclude_planned=True):
    """One clock hour starting at `h0`.

    activities: dicts with `start`, `end` (None = never closed), `loss_class` ('planned' | 'unplanned')
    rates:      the four 15-minute output-rate readings (kg/h) in the hour; None = missing
    Returns {'availability','performance','quality','oee'} as fractions (None where undefined),
    or None when the hour has no OEE (missing data, or nothing planned to run).
    """
    h1 = h0 + timedelta(hours=1)
    if len(rates) != 4 or any(r is None for r in rates) or good_kg is None or reject_kg is None:
        return None
    closed = [a for a in activities if a["end"] is not None]
    planned = _merge(_clip([(a["start"], a["end"]) for a in closed if a["loss_class"] == "planned"], h0, h1))
    everything = _merge(_clip([(a["start"], a["end"]) for a in closed], h0, h1))
    planned_time = 60.0 - _total_min(planned) if exclude_planned else 60.0
    if planned_time <= 0.01:
        return None
    run_time = 60.0 - _total_min(everything)
    availability = max(0.0, run_time / planned_time)
    if run_time <= 0.01:
        return {"availability": 0.0, "performance": None, "quality": None, "oee": 0.0}
    produced = sum(r * BUCKET_MIN / 60.0 for r in rates)
    performance = min(1.0, produced / (ideal_rate * run_time / 60.0))
    total = good_kg + reject_kg
    quality = good_kg / total if total > 0 else None
    oee = availability * performance * quality if quality is not None else None
    return {"availability": availability, "performance": performance, "quality": quality, "oee": oee}
