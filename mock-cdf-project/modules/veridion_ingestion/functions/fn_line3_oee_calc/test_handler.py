"""Runs handler.handle() against a fake CDF client backed by the generated fixtures.

    python3 test_handler.py            (needs cognite-sdk importable)

Checks that the Function, as written, reproduces the OEE rows in line3_oee_hourly.csv from the
process CSV, the MES counts and the SAP notifications. This exercises our code paths, not a real
CDF API: the fake client only mimics the few SDK calls the handler makes.
"""
import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cognite.client.data_classes.data_modeling import ViewId

import handler

PROJECT = Path(__file__).resolve().parents[4]
TS_DIR = PROJECT / "modules/veridion_line3_oee/timeseries"
RAW = PROJECT / "modules/veridion_ingestion/raw/pm_notifications.csv"
UTC = timezone.utc


def parse(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def load(path):
    with open(path, newline="") as f:
        return {parse(r["timestamp"]): r for r in csv.DictReader(f)}


PROCESS, HOURLY = load(TS_DIR / "line3_process_15min.csv"), load(TS_DIR / "line3_oee_hourly.csv")


class Dps:
    def __init__(self, ts, vals, kind):
        self.timestamp = [int(t.timestamp() * 1000) for t in ts]     # Datapoints.timestamp: epoch ms
        setattr(self, kind, list(vals))


class FakeData:
    def __init__(self):
        self.inserted = {}

    def retrieve(self, instance_id, start, end, aggregates, granularity):
        xid = instance_id.external_id
        src = PROCESS if granularity == "15m" else HOURLY
        rows = [(t, r[xid]) for t, r in sorted(src.items()) if start <= t < end and r.get(xid, "") != ""]
        if not rows:
            return None
        ts, vals = zip(*rows)
        return Dps(ts, [float(v) for v in vals], "average" if aggregates == "average" else "sum")

    def insert(self, datapoints, instance_id):
        self.inserted[instance_id.external_id] = dict(datapoints)


class FakeInstances:
    def list(self, instance_type, sources, limit):
        view = sources[0]
        nodes = []
        with open(RAW, newline="") as f:
            for r in csv.DictReader(f):
                s = datetime.strptime(r["ausvn"] + r["auztv"], "%Y%m%d%H%M%S").replace(tzinfo=UTC) - timedelta(hours=1)
                e = (datetime.strptime(r["ausbs"] + r["auztb"], "%Y%m%d%H%M%S").replace(tzinfo=UTC) - timedelta(hours=1)
                     ).isoformat() if r["ausbs"] else None
                props = {"startTime": s.isoformat(), "endTime": e, "lossClass": "planned" if r["qmart"] == "M3" else "unplanned",
                         "assets": [{"space": "sp_veridion_demo", "externalId": "asset_line3"}]}
                nodes.append(type("N", (), {"properties": {view: props}})())
        return nodes


class FakeClient:
    def __init__(self):
        self.time_series = type("T", (), {"data": FakeData()})()
        self.data_modeling = type("D", (), {"instances": FakeInstances()})()


def main():
    checked = bad = 0
    # a window with a full stop + restart, the duplicated notification, a changeover, and the unclosed stop
    for end in ("2026-10-01T00:00:00Z", "2026-10-10T00:00:00Z", "2026-10-15T00:00:00Z", "2026-10-03T08:00:00Z"):
        client = FakeClient()
        out = handler.handle(client, {"hours_back": 48, "end": end})
        for key, ts_xid in handler.OUT.items():
            for h, v in client.time_series.data.inserted[ts_xid].items():
                expected = HOURLY[h][ts_xid]
                checked += 1
                if expected == "" or abs(float(expected) - v) > 0.011:
                    bad += 1
                    print("MISMATCH", ts_xid, h, v, expected)
    print("compared %d datapoints, %d mismatches" % (checked, bad))
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
