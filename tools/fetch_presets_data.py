#!/usr/bin/env python3
"""Download ~2 years of Binance USDT-M futures 15m candles for the preset coins into ./data.
Run in Terminal from the folder that holds this file:  python3 fetch_presets_data.py
Already-downloaded coins are skipped, so you can re-run it after an interruption.
"""
import csv, json, os, time, urllib.request, urllib.error
from datetime import datetime, timezone

COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "LINK", "AVAX", "SUI", "HYPE", "TAO"]
START, END = "2024-10-01", "2026-10-15"
URL = "https://fapi.binance.com/fapi/v1/klines?symbol={s}&interval=15m&startTime={a}&endTime={b}&limit=1500"

def ms(d): return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)

os.makedirs("data", exist_ok=True)
for c in COINS:
    sym = c + "USDT"; out = f"data/{sym}_15m_recent.csv"
    if os.path.exists(out):
        print("skip", out); continue
    a, b, rows = ms(START), ms(END), []
    try:
        while a < b:
            req = urllib.request.Request(URL.format(s=sym, a=a, b=b), headers={"User-Agent": "Mozilla/5.0"})
            batch = json.loads(urllib.request.urlopen(req, timeout=30).read())
            if not batch: break
            rows += [[k[0], k[1], k[2], k[3], k[4], k[5]] for k in batch]
            a = batch[-1][0] + 1
            time.sleep(0.2)
    except urllib.error.HTTPError as e:
        print(f"{sym}: not available ({e.code}), skipped"); continue
    if not rows:
        print(f"{sym}: no data"); continue
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time_ms", "open", "high", "low", "close", "volume"]); w.writerows(rows)
    print(f"saved {out}: {len(rows)} bars from {datetime.fromtimestamp(rows[0][0]/1000, timezone.utc):%Y-%m-%d}")
print("Done.")
