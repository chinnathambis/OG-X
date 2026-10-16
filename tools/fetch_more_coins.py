#!/usr/bin/env python3
"""OG X preset scan, round 2: download ~2 years of Binance USDT-M futures 15m candles into ./data for
  - the top 150 coins by 24h volume, minus the 40 already tested, and
  - the alts on Predictum's "New Era" supported list (1INCH, ATOM, DOT, CRV, GRT ...).
Run in Terminal from the folder that holds this file:  python3 fetch_more_coins.py
Coins already in ./data are skipped, so it can be re-run after an interruption. Takes about 30-40 minutes.
"""
import csv, json, os, time, urllib.request, urllib.error
from datetime import datetime, timezone

TOP_N = 150
DONE = set({'HYPEUSDT', 'AAVEUSDT', 'AKEUSDT', 'AVAXUSDT', 'EGLDUSDT', 'WLDUSDT', 'FILUSDT', 'LTCUSDT', 'PYTHUSDT', 'SUIUSDT', 'ARBUSDT', 'WALUSDT', 'SOLUSDT', 'ENAUSDT', 'BNBUSDT', 'ONDOUSDT', 'TRUMPUSDT', 'PUMPUSDT', 'QUSDT', 'UNIUSDT', 'ADAUSDT', 'ETHUSDT', 'STRKUSDT', 'NEARUSDT', 'PAXGUSDT', 'ZEREBROUSDT', '1000PEPEUSDT', 'XRPUSDT', 'ZECUSDT', 'OPUSDT', 'BTWUSDT', 'LINKUSDT', 'ARCUSDT', 'INJUSDT', 'DOGEUSDT', 'BTCUSDT', 'QNTUSDT', 'TAOUSDT', 'ZKUSDT', 'BCHUSDT'})   # already tested (round 1)
EXTRA = ['1000SHIBUSDT', '1INCHUSDT', 'ALICEUSDT', 'ALPHAUSDT', 'API3USDT', 'ARPAUSDT', 'ATAUSDT', 'ATOMUSDT', 'AXSUSDT', 'BAKEUSDT', 'BANDUSDT', 'BELUSDT', 'CHZUSDT', 'COMPUSDT', 'COTIUSDT', 'CRVUSDT', 'DASHUSDT', 'DENTUSDT', 'DOTUSDT', 'DUSKUSDT', 'DYDXUSDT', 'ENJUSDT', 'FLOWUSDT', 'GRTUSDT']   # Predictum New Era list
START, END = "2024-10-01", "2026-10-15"
API = "https://fapi.binance.com"
SKIP = {"USDCUSDT", "FDUSDUSDT", "BTCDOMUSDT"}           # stablecoins / index contracts

def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

def ms(d): return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)

perps = {s["symbol"] for s in get("/fapi/v1/exchangeInfo")["symbols"]
         if s["contractType"] == "PERPETUAL" and s["quoteAsset"] == "USDT" and s["status"] == "TRADING"}
tick = sorted((t for t in get("/fapi/v1/ticker/24hr") if t["symbol"] in perps and t["symbol"] not in SKIP),
              key=lambda t: float(t["quoteVolume"]), reverse=True)
coins = [t["symbol"] for t in tick[:TOP_N] if t["symbol"] not in DONE]
coins += [c for c in EXTRA if c in perps and c not in coins and c not in DONE]
print(len(coins), "coins to download:", ", ".join(coins), flush=True)

os.makedirs("data", exist_ok=True)
for n, sym in enumerate(coins, 1):
    out = f"data/{sym}_15m_recent.csv"
    if os.path.exists(out):
        print(f"[{n}/{len(coins)}] skip {sym} (already downloaded)"); continue
    a, b, rows = ms(START), ms(END), []
    try:
        while a < b:
            batch = get(f"/fapi/v1/klines?symbol={sym}&interval=15m&startTime={a}&endTime={b}&limit=1500")
            if not batch: break
            rows += [[k[0], k[1], k[2], k[3], k[4], k[5]] for k in batch]
            a = batch[-1][0] + 1
            time.sleep(0.15)
    except urllib.error.HTTPError as e:
        print(f"[{n}/{len(coins)}] {sym}: error {e.code}, skipped"); continue
    if not rows:
        print(f"[{n}/{len(coins)}] {sym}: no data"); continue
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time_ms", "open", "high", "low", "close", "volume"]); w.writerows(rows)
    print(f"[{n}/{len(coins)}] saved {sym}: {len(rows)} bars from {datetime.fromtimestamp(rows[0][0]/1000, timezone.utc):%Y-%m-%d}", flush=True)
print("Done.")
