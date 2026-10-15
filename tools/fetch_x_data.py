#!/usr/bin/env python3
"""Download Bybit USDT perpetual 15m candles around each Predictum X signal (research/x/x_signals.csv)
into ./data_bybit. Run in Terminal from the folder that holds this file:  python3 fetch_x_data.py
Window per signal: 90 days before to 5 days after. Takes 1-3 minutes.
"""
import csv, json, os, time, urllib.request
from datetime import datetime, timezone, timedelta

SIGNALS = [  # coin, signal time UTC (from the post ID)
    ("ZEREBRO", "2026-05-25 09:45"), ("GRIFFAIN", "2026-05-22 07:30"), ("BANANA", "2026-05-21 19:30"),
    ("GUN", "2026-05-06 14:15"), ("GOAT", "2026-04-29 09:45"), ("GPS", "2026-03-31 03:00"),
    ("AVAAI", "2026-03-05 03:00"), ("BERA", "2026-02-26 03:00"), ("XCN", "2026-02-15 03:45"),
    ("JELLYJELLY", "2026-02-07 09:45"), ("DOOD", "2026-01-04 03:45"), ("FARTCOIN", "2025-12-06 14:15"),
    ("VANA", "2025-11-29 12:00"), ("AVL", "2025-10-24 06:45"),
]
URL = "https://api.bybit.com/v5/market/kline?category=linear&symbol={s}&interval=15&start={a}&end={b}&limit=1000"
os.makedirs("data_bybit", exist_ok=True)
for coin, ts in SIGNALS:
    sym = coin + "USDT"
    t = datetime.strptime(ts, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    a0 = int((t - timedelta(days=90)).timestamp() * 1000); end = int((t + timedelta(days=5)).timestamp() * 1000)
    out = f"data_bybit/{sym}_15m_{t:%Y%m%d}.csv"
    if os.path.exists(out):
        print("skip", out); continue
    rows = {}; b = end
    while b > a0:   # Bybit returns newest first; page backwards
        req = urllib.request.Request(URL.format(s=sym, a=a0, b=b), headers={"User-Agent": "Mozilla/5.0"})
        res = json.loads(urllib.request.urlopen(req, timeout=30).read())
        lst = res.get("result", {}).get("list", [])
        if not lst: break
        for k in lst: rows[int(k[0])] = k[:6]
        oldest = min(int(k[0]) for k in lst)
        if oldest <= a0 or len(lst) < 1000: break
        b = oldest - 1
        time.sleep(0.15)
    if not rows:
        print(f"{sym}: no data ({res.get('retMsg')})"); continue
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time_ms", "open", "high", "low", "close", "volume"])
        for k in sorted(rows): w.writerow(rows[k])
    print(f"saved {out}: {len(rows)} bars", flush=True)
print("Done.")
