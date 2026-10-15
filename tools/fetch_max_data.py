#!/usr/bin/env python3
"""Download the FULL Binance USDT-M futures 15m history (from listing) for the preset coins into ./data.
Run in Terminal from the folder that holds this file:  python3 fetch_max_data.py
Takes ~10 minutes. Re-running resumes: finished coins are skipped.
"""
import csv, json, os, time, urllib.request, urllib.error
from datetime import datetime, timezone

COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "LINK", "AVAX", "SUI", "HYPE", "TAO",
         "LTC", "DOT", "NEAR", "ATOM", "TRX", "BCH", "AAVE", "UNI", "FIL", "INJ", "OP", "ARB"]
START = "2019-09-01"
URL = "https://fapi.binance.com/fapi/v1/klines?symbol={s}&interval=15m&startTime={a}&limit=1500"

def ms(d): return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)

os.makedirs("data", exist_ok=True)
now = int(time.time() * 1000)
for c in COINS:
    sym = c + "USDT"; out = f"data/{sym}_15m_max.csv"
    if os.path.exists(out):
        print("skip", out); continue
    a, rows = ms(START), []
    try:
        while a < now:
            req = urllib.request.Request(URL.format(s=sym, a=a), headers={"User-Agent": "Mozilla/5.0"})
            batch = json.loads(urllib.request.urlopen(req, timeout=30).read())
            if not batch: break
            rows += [[k[0], k[1], k[2], k[3], k[4], k[5]] for k in batch]
            a = batch[-1][0] + 1
            if len(batch) < 1500: break
            time.sleep(0.15)
    except urllib.error.HTTPError as e:
        print(f"{sym}: not available ({e.code}), skipped"); continue
    if not rows:
        print(f"{sym}: no data"); continue
    tmp = out + ".part"
    with open(tmp, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time_ms", "open", "high", "low", "close", "volume"]); w.writerows(rows)
    os.replace(tmp, out)
    print(f"saved {out}: {len(rows)} bars from {datetime.fromtimestamp(rows[0][0]/1000, timezone.utc):%Y-%m-%d}", flush=True)
print("Done.")
