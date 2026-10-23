"""CDF Function entry point: write hourly OEE for Production Line 3.

ILLUSTRATIVE. This file documents how the OEE series in this mock project would be produced.
It has never been run against a CDF project (there is none). The calculation itself lives in
oee.py and is exercised by fixtures/generate_datapoints.py.
"""
from datetime import datetime, timedelta, timezone

from cognite.client.data_classes.data_modeling import NodeId, ViewId

from oee import IDEAL_RATE_SOP_REV_B, compute_hour

SPACE = "sp_veridion_demo"
RATE_TS = "ts_line3_output_rate_kg_per_hr"
GOOD_TS = "ts_line3_good_output_kg"
REJECT_TS = "ts_line3_reject_output_kg"
OUT = {
    "oee": "ts_line3_oee_pct",
    "availability": "ts_line3_availability_pct",
    "performance": "ts_line3_performance_pct",
    "quality": "ts_line3_quality_pct",
}


def handle(client, data):
    """data: {"hours_back": 6, "end": optional ISO hour}. Recomputes the trailing window; safe to re-run
    (datapoints are upserted). `end` defaults to the current hour; set it to backfill."""
    if data.get("end"):
        end = datetime.fromisoformat(data["end"].replace("Z", "+00:00"))
    else:
        end = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(hours=int(data.get("hours_back", 6)))

    activities = _load_activities(client, start - timedelta(hours=12), end)
    rates = _series(client, RATE_TS, start, end, "15m")
    good = _series(client, GOOD_TS, start, end, "1h")
    reject = _series(client, REJECT_TS, start, end, "1h")

    written = {k: [] for k in OUT}
    h0 = start
    while h0 < end:
        buckets = [rates.get(h0 + timedelta(minutes=15 * i)) for i in range(4)]
        res = compute_hour(h0, activities, buckets, good.get(h0), reject.get(h0),
                           ideal_rate=IDEAL_RATE_SOP_REV_B, exclude_planned=True)
        if res:
            for key, ts_xid in OUT.items():
                if res[key] is not None:
                    written[key].append((h0, round(res[key] * 100, 2)))
        h0 += timedelta(hours=1)

    for key, ts_xid in OUT.items():
        client.time_series.data.insert(written[key], instance_id=NodeId(SPACE, ts_xid))
    return {k: len(v) for k, v in written.items()}


def _series(client, xid, start, end, granularity):
    """{bucket start (UTC): value}. `retrieve` returns Datapoints: .timestamp is epoch milliseconds, and
    aggregate results expose .average / .sum, not .value."""
    use_avg = granularity == "15m"
    dps = client.time_series.data.retrieve(instance_id=NodeId(SPACE, xid), start=start, end=end,
                                           aggregates="average" if use_avg else "sum", granularity=granularity)
    if dps is None:
        return {}
    values = dps.average if use_avg else dps.sum
    return {_to_utc(t): float(v) for t, v in zip(dps.timestamp, values) if v == v}


def _to_utc(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def _load_activities(client, start, end):
    """Line 3 activities from VeridionDowntimeActivity. Not windowed: compute_hour clips to the hour."""
    view = ViewId("sp_veridion_dm", "VeridionDowntimeActivity", "v1")
    out = []
    for n in client.data_modeling.instances.list(instance_type="node", sources=[view], limit=-1):
        p = n.properties[view]
        on_line3 = any(a.get("externalId") == "asset_line3" for a in p.get("assets") or [])
        if not p.get("startTime") or not on_line3:
            continue
        out.append({
            "start": datetime.fromisoformat(p["startTime"]),
            "end": datetime.fromisoformat(p["endTime"]) if p.get("endTime") else None,
            "loss_class": p.get("lossClass"),
        })
    return out
