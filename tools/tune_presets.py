#!/usr/bin/env python3
"""Tune OG Breakout per coin on 45m bars built from data/<SYM>_15m_recent.csv.
Realised model: exit at the stop or at the next signal's entry price, 0.08% round-trip fees, 1x.
Train = everything before SPLIT, test = SPLIT onwards. Picks by train score, reports test, checks neighbours.
"""
import os, sys, itertools
import numpy as np, pandas as pd

DATA = os.environ.get("PREDICTUM_DATA", "data")
SPLIT = pd.Timestamp("2026-01-01")
NS   = list(range(60, 401, 10)) + list(range(420, 701, 20))
BUFS = [0.0, 0.003, 0.006, 0.01]
SLS  = [0.03, 0.04, 0.05, 0.06, 0.08, 0.10]
FEE  = 0.0008

def load45(sym):
    d = pd.read_csv(os.path.join(DATA, f"{sym}_15m_recent.csv"))
    d["t"] = pd.to_datetime(d.time_ms, unit="ms"); d = d.set_index("t")
    return d.resample("45min", origin="start_day", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()

def run(b, N, buf, sl):
    H, L, O, C = b.high.values, b.low.values, b.open.values, b.close.values
    up = b.high.rolling(N).max().shift(1).values * (1 - buf)
    dn = b.low.rolling(N).min().shift(1).values * (1 + buf)
    pos = 0; ent = 0.0; trades = []   # (entry index, return)
    cur = None
    for i in range(N + 1, len(b)):
        if pos == 1 and L[i] <= ent * (1 - sl):
            trades.append((cur, -sl - FEE)); pos = 0; cur = None
        elif pos == -1 and H[i] >= ent * (1 + sl):
            trades.append((cur, -sl - FEE)); pos = 0; cur = None
        if H[i] >= up[i] and pos != 1:
            px = max(O[i], up[i])
            if pos == -1: trades.append((cur, ent / px - 1 - FEE))
            pos, ent, cur = 1, px, i
        elif L[i] <= dn[i] and pos != -1:
            px = min(O[i], dn[i])
            if pos == 1: trades.append((cur, px / ent - 1 - FEE))
            pos, ent, cur = -1, px, i
    if pos != 0:
        trades.append((cur, (C[-1] / ent - 1) * pos - FEE))
    return trades

def stats(rets):
    r = np.array(rets)
    if len(r) == 0: return dict(n=0, net=0, dd=0, pf=0, win=0)
    eq = np.cumprod(1 + r); dd = (1 - eq / np.maximum.accumulate(eq)).max()
    g, l = r[r > 0].sum(), -r[r < 0].sum()
    return dict(n=len(r), net=eq[-1] - 1, dd=dd, pf=g / l if l > 0 else 9.99, win=(r > 0).mean())

def tune(sym):
    b = load45(sym); idx = b.index; rows = []
    for N, buf, sl in itertools.product(NS, BUFS, SLS):
        tr = run(b, N, buf, sl)
        a = [r for i, r in tr if idx[i] < SPLIT]; t = [r for i, r in tr if idx[i] >= SPLIT]
        sa, st = stats(a), stats(t)
        score = sa["net"] / max(sa["dd"], 0.05) if sa["n"] >= 12 else -9
        rows.append(dict(N=N, buf=buf, sl=sl, score=score, **{f"tr_{k}": v for k, v in sa.items()}, **{f"te_{k}": v for k, v in st.items()}))
    R = pd.DataFrame(rows)
    # neighbour robustness: mean train score of same buf/sl and N within ±2 grid steps
    R["nb"] = R.groupby(["buf", "sl"])["score"].transform(lambda s: s.rolling(5, center=True, min_periods=3).mean())
    R["pick"] = np.minimum(R.score, R.nb)
    best = R.sort_values("pick", ascending=False).iloc[0]
    return b, R, best

if __name__ == "__main__":
    syms = sys.argv[1:] or sorted(f.split("_")[0] for f in os.listdir(DATA) if f.endswith("_15m_recent.csv"))
    out = []
    for s in syms:
        b, R, x = tune(s)
        out.append(dict(sym=s, first=b.index[0].date(), N=int(x.N), buf=x.buf, sl=x.sl,
                        tr_n=int(x.tr_n), tr_net=round(100 * x.tr_net), tr_dd=round(100 * x.tr_dd), tr_pf=round(x.tr_pf, 2), tr_win=round(100 * x.tr_win),
                        te_n=int(x.te_n), te_net=round(100 * x.te_net), te_dd=round(100 * x.te_dd), te_pf=round(x.te_pf, 2), te_win=round(100 * x.te_win)))
        print(out[-1], flush=True)
    pd.DataFrame(out).to_csv("tune_results.csv", index=False)
