#!/usr/bin/env python3
"""Generate the datapoint fixtures for the Veridion mock CDF project (deterministic, stdlib only).

    python3 mock-cdf-project/fixtures/generate_datapoints.py

Reads   modules/veridion_ingestion/raw/pm_notifications.csv  (SAP PM notifications, local time)
Writes  modules/veridion_line3_oee/timeseries/line3_process_15min.csv
        modules/veridion_line3_oee/timeseries/line3_oee_hourly.csv

The process signals, MES counts and downtime windows are simulated. The OEE series are then
*computed* from them with the same oee.py the CDF Function uses, so
oee = availability x performance x quality holds in every row and the numbers are checkable.

The window is 2026-09-15 to 2026-10-14 (UTC). Seed is fixed; re-running reproduces the files.
"""
import csv
import math
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
sys.path.insert(0, str(PROJECT / "modules/veridion_ingestion/functions/fn_line3_oee_calc"))
from oee import IDEAL_RATE_MES_LEGACY, IDEAL_RATE_SOP_REV_B, compute_hour  # noqa: E402

UTC = timezone.utc
START = datetime(2026, 9, 15, tzinfo=UTC)
END = datetime(2026, 10, 15, tzinfo=UTC)
BST_OFFSET = timedelta(hours=1)          # Europe/London is UTC+1 for the whole window (BST ends 2026-10-25)
RNG = random.Random(20261016)

RAW = PROJECT / "modules/veridion_ingestion/raw/pm_notifications.csv"
OUT = PROJECT / "modules/veridion_line3_oee/timeseries"

# Hand-placed behaviours (documented in the project README, "Known data characteristics")
OPEN_ENDED_ACTUAL_MIN = 25                       # unclosed SAP notification: stop really lasted this long
FV301_FAULTS = {"000400118802": 3.0, "000400119318": 2.5}       # notification -> hours of precursor
DIE_TRIP = {"000400118377": 1.5}                                # notification -> hours of precursor
MICRO_STOPS = [("2026-09-16T10:12", 5), ("2026-09-18T16:40", 4), ("2026-09-22T03:27", 7), ("2026-09-25T21:05", 3),
               ("2026-09-27T12:50", 8), ("2026-10-02T07:33", 5), ("2026-10-05T18:18", 6), ("2026-10-08T01:44", 4),
               ("2026-10-11T14:09", 7), ("2026-10-13T09:51", 5)]       # never logged in SAP
OPC_GAP = (datetime(2026, 10, 3, 2, 10, tzinfo=UTC), datetime(2026, 10, 3, 5, 50, tzinfo=UTC))
FLATLINE = ("ts_reactor_r301_pressure_bar", datetime(2026, 10, 8, 4, tzinfo=UTC), datetime(2026, 10, 8, 10, tzinfo=UTC))
SPIKE = ("ts_extruder_ex302_melt_temperature_degc", datetime(2026, 9, 24, 11, 15, tzinfo=UTC), 9999.0)


def local_to_utc(date, time):
    return datetime.strptime(date + time, "%Y%m%d%H%M%S").replace(tzinfo=UTC) - BST_OFFSET


def load_activities():
    acts = []
    with open(RAW, newline="") as f:
        for r in csv.DictReader(f):
            start = local_to_utc(r["ausvn"], r["auztv"])
            end = local_to_utc(r["ausbs"], r["auztb"]) if r["ausbs"] else None
            acts.append({"id": r["qmnum"], "start": start, "end": end,
                         "loss_class": "planned" if r["qmart"] == "M3" else "unplanned"})
    return acts


def merged(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def frac_in(intervals, t0, t1):
    tot = sum(max(0.0, (min(e, t1) - max(s, t0)).total_seconds()) for s, e in intervals)
    return tot / (t1 - t0).total_seconds()


def r1(x):
    return round(x, 1)


def main():
    acts = load_activities()
    # Real downtime windows used to drive the simulation (unclosed notification gets its true end).
    windows = []
    for a in acts:
        end = a["end"] or a["start"] + timedelta(minutes=OPEN_ENDED_ACTUAL_MIN)
        windows.append((a["start"], end))
    stops = merged(windows)
    micro = [(datetime.fromisoformat(s).replace(tzinfo=UTC), datetime.fromisoformat(s).replace(tzinfo=UTC) + timedelta(minutes=m))
             for s, m in MICRO_STOPS]
    fv_pre = [(a["start"] - timedelta(hours=FV301_FAULTS[a["id"]]), a["start"]) for a in acts if a["id"] in FV301_FAULTS]
    die_pre = [(a["start"] - timedelta(hours=DIE_TRIP[a["id"]]), a["start"]) for a in acts if a["id"] in DIE_TRIP]
    restart_ends = [e for _, e in stops]

    buckets = []
    t = START
    while t < END:
        buckets.append(t)
        t += timedelta(minutes=15)

    cols = ["ts_line3_output_rate_kg_per_hr", "ts_reactor_r301_temperature_degc", "ts_reactor_r301_temperature_b_degf",
            "ts_reactor_r301_pressure_bar", "ts_reactor_r301_agitator_current_a", "ts_reactor_r301_feed_valve_fv301_position_pct",
            "ts_reactor_r301_jacket_coolant_flow_m3h", "ts_extruder_ex302_screw_speed_rpm", "ts_extruder_ex302_motor_load_pct",
            "ts_extruder_ex302_melt_temperature_degc", "ts_extruder_ex302_die_pressure_bar"]
    rows, temp, melt = {}, 182.0, 238.0
    for t in buckets:
        t1 = t + timedelta(minutes=15)
        stopped = frac_in(stops, t, t1)
        micro_f = frac_in(micro, t, t1)
        ramp = 0.65 if any(timedelta(0) <= t - e < timedelta(minutes=30) for e in restart_ends) else 1.0
        days = (t - START).total_seconds() / 86400
        nominal = 3350 + 55 * math.sin(2 * math.pi * days / 7)
        rate = nominal * (1 - stopped) * (1 - micro_f) * ramp * (1 + RNG.gauss(0, 0.012))
        down = stopped > 0.5
        temp += ((150.0 if down else 182.0) - temp) * (1 - math.exp(-15 / 40))
        melt += ((190.0 if down else 238.0) - melt) * (1 - math.exp(-15 / 40))
        drift = 0.0
        for s, e in fv_pre:
            if s <= t < e:
                drift = 7.0 * (t - s).total_seconds() / (e - s).total_seconds()
        t_a = temp + drift + RNG.gauss(0, 0.5) + 0.8 * math.sin(2 * math.pi * days)
        fv_pos = RNG.gauss(55, 2.5)
        if any(s <= t < e for s, e in fv_pre if (e - s) >= timedelta(hours=2)):
            fv_pos = 55.0
        if down:
            fv_pos = 0.0
        die = RNG.gauss(78, 1.5)
        for s, e in die_pre:
            if s <= t < e:
                die += 17.0 * (t - s).total_seconds() / (e - s).total_seconds()
        if down:
            die = 5.0 + RNG.gauss(0, 0.3)
        press = 14.2 + RNG.gauss(0, 0.1) if not down else 11.0 + RNG.gauss(0, 0.2)
        if FLATLINE[1] <= t < FLATLINE[2]:
            press = 14.2
        screw = (310 + RNG.gauss(0, 1.2)) * (1 - stopped) * (1 - micro_f)
        rows[t] = {
            cols[0]: r1(max(rate, 0)), cols[1]: r1(t_a), cols[2]: r1((t_a + RNG.gauss(0, 0.3)) * 9 / 5 + 32 + 0.4),
            cols[3]: round(press, 2), cols[4]: r1(18 + RNG.gauss(0, 0.3) if down else 42 + RNG.gauss(0, 0.4)),
            cols[5]: r1(fv_pos), cols[6]: r1(60 + RNG.gauss(0, 1.5) if down else 118 + RNG.gauss(0, 2)),
            cols[7]: r1(max(screw, 0)), cols[8]: r1(12 + RNG.gauss(0, 1) if down else 68 + RNG.gauss(0, 1.5)),
            cols[9]: r1(melt + RNG.gauss(0, 0.8)), cols[10]: r1(die),
        }
        if t == SPIKE[1]:
            rows[t][SPIKE[0]] = SPIKE[2]

    # MES hourly counts come from the same underlying production, independent of the OPC UA gap.
    hours = []
    h = START
    while h < END:
        hours.append(h)
        h += timedelta(hours=1)
    counts = {}
    for h in hours:
        produced = sum(rows[h + timedelta(minutes=15 * i)][cols[0]] * 0.25 for i in range(4)) * (1 + RNG.gauss(0, 0.003))
        q = 0.982 + RNG.gauss(0, 0.004)
        for _, e in stops:
            if timedelta(0) <= h - e < timedelta(hours=2):
                q = min(q, 0.93 + RNG.gauss(0, 0.01))
            elif timedelta(hours=2) <= h - e < timedelta(hours=3):
                q = min(q, 0.96)
        good = produced * min(q, 0.999)
        counts[h] = (r1(good), r1(max(produced - good, 0)))

    # Write the process file, blanking the OPC UA gap.
    OUT.mkdir(parents=True, exist_ok=True)
    recorded = {}
    with open(OUT / "line3_process_15min.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp"] + cols)
        for t in buckets:
            gap = OPC_GAP[0] <= t + timedelta(minutes=15) - timedelta(seconds=1) and t < OPC_GAP[1]
            vals = [None if gap else rows[t][c] for c in cols]
            recorded[t] = vals
            w.writerow([t.strftime("%Y-%m-%dT%H:%M:%SZ")] + ["" if v is None else v for v in vals])

    # OEE from the recorded data, using the shared calculation.
    oee_cols = ["ts_line3_oee_pct", "ts_line3_availability_pct", "ts_line3_performance_pct", "ts_line3_quality_pct",
                "ts_line3_oee_pct_mes_legacy", "ts_line3_good_output_kg", "ts_line3_reject_output_kg",
                "ts_line1_oee_pct_mes_legacy", "ts_line2_oee_pct_mes_legacy", "ts_line4_oee_pct_mes_legacy"]
    out_rows, n_oee, worst = [], 0, 0.0
    for h in hours:
        rates = [recorded[h + timedelta(minutes=15 * i)][0] for i in range(4)]
        good, reject = counts[h]
        sop = compute_hour(h, acts, rates, good, reject, IDEAL_RATE_SOP_REV_B, True)
        leg = compute_hour(h, acts, rates, good, reject, IDEAL_RATE_MES_LEGACY, False)
        row = {c: "" for c in oee_cols}
        if sop and sop["oee"] is not None:
            for key, col in (("oee", 0), ("availability", 1), ("performance", 2), ("quality", 3)):
                if sop[key] is not None:
                    row[oee_cols[col]] = round(sop[key] * 100, 2)
            if sop["performance"] is not None:
                worst = max(worst, abs(sop["oee"] - sop["availability"] * sop["performance"] * sop["quality"]))
            n_oee += 1
        if leg and leg["oee"] is not None:
            row["ts_line3_oee_pct_mes_legacy"] = round(leg["oee"] * 100, 2)
        row["ts_line3_good_output_kg"], row["ts_line3_reject_output_kg"] = good, reject
        day = (h - START).total_seconds() / 86400
        for n, base in ((1, 71.0), (2, 77.5), (4, 74.0)):
            v = base + 3.0 * math.sin(2 * math.pi * day / 7 + n) + RNG.gauss(0, 2.2)
            row["ts_line%d_oee_pct_mes_legacy" % n] = round(min(max(v, 35.0), 96.0), 2)
        out_rows.append((h, row))
    with open(OUT / "line3_oee_hourly.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp"] + oee_cols)
        for h, row in out_rows:
            w.writerow([h.strftime("%Y-%m-%dT%H:%M:%SZ")] + [row[c] for c in oee_cols])
    print("process rows: %d, hourly rows: %d, hours with SOP OEE: %d, max |OEE - AxPxQ| = %.2e"
          % (len(buckets), len(hours), n_oee, worst))


if __name__ == "__main__":
    main()
