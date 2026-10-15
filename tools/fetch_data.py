#!/usr/bin/env python3
"""Download Binance USDT-M futures candles (free, no account) into ./data as CSV.
Run from the repo root:  python3 tools/fetch_data.py
"""
import csv, json, os, time, urllib.request
from datetime import datetime, timezone

JOBS = [  # symbol, interval, start, end (UTC)
    ("BTCUSDT", "15m", "2020-01-01", "2022-03-01"),
    ("ETHUSDT", "15m", "2021-01-01", "2023-04-01"),
]
URL = "https://fapi.binance.com/fapi/v1/klines?symbol={s}&interval={i}&startTime={a}&endTime={b}&limit=1500"

def ms(d): return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)

os.makedirs("data", exist_ok=True)
for sym, iv, start, end in JOBS:
    out = f"data/{sym}_{iv}.csv"
    a, b, rows = ms(start), ms(end), []
    while a < b:
        req = urllib.request.Request(URL.format(s=sym, i=iv, a=a, b=b), headers={"User-Agent": "Mozilla/5.0"})
        batch = json.loads(urllib.request.urlopen(req, timeout=30).read())
        if not batch: break
        rows += [[k[0], k[1], k[2], k[3], k[4], k[5]] for k in batch]
        a = batch[-1][0] + 1
        print(f"{sym} {iv}: {len(rows)} bars, up to {datetime.fromtimestamp(batch[-1][0]/1000, timezone.utc):%Y-%m-%d}")
        time.sleep(0.25)
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time_ms", "open", "high", "low", "close", "volume"]); w.writerows(rows)
    print("saved", out)
print("Done.")
