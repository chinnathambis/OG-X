#!/usr/bin/env python3
"""Exit-rule study for OG Breakout. Entry engine unchanged; only the way a trade is closed changes.
Train = before 2026-01-01, test = 2026. Realised, 1x, 0.08% round-trip fees (scaled by the share closed).
"""
import os, sys, itertools
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tune_presets import load45, stats, SPLIT, FEE

def run_exit(b, N, buf, sl, mode, ladder=(0.01, 0.02, 0.03, 0.04, 0.08), split=(0.2, 0.2, 0.2, 0.2, 0.2),
             be_after=0, trail=0.0, htf=0):
    """mode: 'flip' (baseline), 'ladder' (partial exits at TPs, rest to flip/stop), 'be' (stop->entry after TP be_after),
    'trail' (trailing stop trail% from best price once in profit), combined via args. htf>0: only trade with the trend of an N*htf channel midline."""
    H, L, O, C = b.high.values, b.low.values, b.open.values, b.close.values
    up = b.high.rolling(N).max().shift(1).values * (1 - buf)
    dn = b.low.rolling(N).min().shift(1).values * (1 + buf)
    if htf:
        mid = ((b.high.rolling(N * htf).max() + b.low.rolling(N * htf).min()) / 2).shift(1).values
    full_exit_bar = -1; pos = 0; ent = 0.0; stop = 0.0; best = 0.0; rem = 1.0; acc = 0.0; tpi = 0; cur = None; out = []
    def close_at(px):
        nonlocal acc
        acc += rem * ((px / ent - 1) * pos)
    for i in range(N * max(htf, 1) + 1, len(b)):
        # manage open trade
        if pos != 0:
            # stop first (conservative)
            if (pos == 1 and L[i] <= stop) or (pos == -1 and H[i] >= stop):
                close_at(stop); out.append((cur, acc - FEE)); pos = 0
            else:
                fav = H[i] if pos == 1 else L[i]
                best = max(best, fav) if pos == 1 else min(best, fav)
                while tpi < len(ladder) and ((pos == 1 and H[i] >= ent * (1 + ladder[tpi])) or (pos == -1 and L[i] <= ent / (1 + ladder[tpi]))):
                    px = ent * (1 + ladder[tpi]) if pos == 1 else ent / (1 + ladder[tpi])
                    if mode in ("ladder",):
                        q = split[tpi]; p_ = ladder[tpi]; acc += q * (p_ if pos == 1 else p_ / (1 + p_)); rem -= q
                    tpi += 1
                    if be_after and tpi == be_after:
                        stop = max(stop, ent) if pos == 1 else min(stop, ent)
                if rem <= 1e-9:
                    out.append((cur, acc - FEE)); pos = 0; full_exit_bar = i
                elif trail:
                    t = best * (1 - trail) if pos == 1 else best * (1 + trail)
                    if (pos == 1 and t > stop and best > ent) or (pos == -1 and t < stop and best < ent):
                        stop = t
        # signals
        lt = H[i] >= up[i] and pos != 1; st = L[i] <= dn[i] and pos != -1 and not lt
        if i == full_exit_bar:   # no re-entry on the bar the last target filled
            lt = st = False
        if htf and not np.isnan(mid[i]):
            lt = lt and C[i - 1] > mid[i]; st = st and C[i - 1] < mid[i] and not lt
        if lt or st:
            d = 1 if lt else -1; px = max(O[i], up[i]) if lt else min(O[i], dn[i])
            if pos != 0:
                close_at(px); out.append((cur, acc - FEE))
            pos, ent, cur, rem, acc, tpi = d, px, i, 1.0, 0.0, 0
            best = px; stop = px * (1 - sl) if d == 1 else px * (1 + sl)
    if pos != 0:
        close_at(C[-1]); out.append((cur, acc - FEE))
    return out

VARIANTS = {
    "baseline (hold to stop / flip)": dict(mode="flip"),
    "BE after TP1 (1%)":              dict(mode="flip", be_after=1),
    "BE after TP2 (2%)":              dict(mode="flip", be_after=2),
    "BE after TP3 (3%)":              dict(mode="flip", be_after=3),
    "ladder 20% each 1/2/3/4/8":      dict(mode="ladder"),
    "ladder + BE after TP2":          dict(mode="ladder", be_after=2),
    "ladder 10/10/10/20/20 (40% runs)": dict(mode="ladder", split=(0.1, 0.1, 0.1, 0.2, 0.2)),
    "trail 5% after profit":          dict(mode="flip", trail=0.05),
    "trail 8% after profit":          dict(mode="flip", trail=0.08),
    "trail 12% after profit":         dict(mode="flip", trail=0.12),
    "trend filter (3x channel)":      dict(mode="flip", htf=3),
    "trend filter + BE after TP2":    dict(mode="flip", htf=3, be_after=2),
}

if __name__ == "__main__":
    PRESETS = [("Universal", 500, 0.006, 0.03), ("Fast", 60, 0.0, 0.10), ("Swing450", 450, 0.01, 0.03), ("Slow800", 800, 0.01, 0.03)]
    syms = sys.argv[1:] or sorted(f.split("_")[0] for f in os.listdir(os.environ.get("PREDICTUM_DATA", "data")) if f.endswith("_15m_recent.csv"))
    rows = []
    for s in syms:
        b = load45(s); idx = b.index
        for (pn, N, buf, sl), (vn, kw) in itertools.product(PRESETS, VARIANTS.items()):
            tr = run_exit(b, N, buf, sl, **kw)
            a = stats([r for i, r in tr if idx[i] < SPLIT]); t = stats([r for i, r in tr if idx[i] >= SPLIT])
            rows.append(dict(sym=s, preset=pn, variant=vn, **{"a_" + k: v for k, v in a.items()}, **{"t_" + k: v for k, v in t.items()}))
        print(s, flush=True)
    pd.DataFrame(rows).to_csv("exit_study.csv", index=False)
