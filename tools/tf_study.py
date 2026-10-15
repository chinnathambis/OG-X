#!/usr/bin/env python3
"""Timeframe study: same engine on 15m/30m/45m/1h/2h/4h. Channel length is set in DAYS so timeframes compare fairly.
Train before 2026-01-01, test 2026. Realised, 1x, 0.08% fees. Writes tf_grid_<SYM>.csv."""
import os, sys, itertools
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tune_presets as t

TFS = {"15m": 15, "30m": 30, "45m": 45, "1h": 60, "2h": 120, "4h": 240}
DAYS = [1, 2, 3, 5, 7, 10, 14, 18, 22, 26]
BUFS = [0.0, 0.003, 0.006, 0.01, 0.015]
SLS = [0.03, 0.04, 0.06, 0.08, 0.10]

def load(sym, minutes):
    d = pd.read_csv(os.path.join(t.DATA, f"{sym}_15m_recent.csv")); d["t"] = pd.to_datetime(d.time_ms, unit="ms"); d = d.set_index("t")
    if minutes == 15: return d[["open", "high", "low", "close"]]
    return d.resample(f"{minutes}min", origin="start_day", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()

if __name__ == "__main__":
    sym = sys.argv[1]; rows = []
    for tf, m in TFS.items():
        b = load(sym, m); idx = b.index; per_day = 1440 // m
        for days, buf, sl in itertools.product(DAYS, BUFS, SLS):
            N = max(10, days * per_day)
            tr = t.run(b, N, buf, sl)
            a = t.stats([r for i, r in tr if idx[i] < t.SPLIT]); e = t.stats([r for i, r in tr if idx[i] >= t.SPLIT])
            rows.append(dict(sym=sym, tf=tf, days=days, N=N, buf=buf, sl=sl, **{"a_" + k: v for k, v in a.items()}, **{"e_" + k: v for k, v in e.items()}))
    pd.DataFrame(rows).to_csv(f"tf_grid_{sym}.csv", index=False)
