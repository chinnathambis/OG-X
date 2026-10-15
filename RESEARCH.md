# Predictum — reverse-engineering research (2026-10-15)

## SOLVED: the signal engine (fitted on Binance USDT-M futures OHLCV)
The engine is a Donchian channel breakout (Turtle-style), computed on 45-minute bars:
- Long level  = highest(high, N)[1] × (1 − buf)
- Short level = lowest(low, N)[1]  × (1 + buf)
- Entry fills **intrabar** when price touches the level. Entry price = max(open, level) for longs and min(open, level) for shorts. No bar close is needed.
- One position at a time. An opposite touch flips the position.
- After a stop-loss, a same-side re-entry happens on the next touch of that side's level. Take-profits do not close the position, so they don't free it for re-entry.
- Peak-profit label = 10 × (maxHigh/entry − 1) for longs, and 10 × (entry/minLow − 1) for shorts, measured until the next signal (including after a stop). It is shown as −SL×10 only when the SL was hit and the peak never reached TP1 (0.3%). The stats-table percentages are leveraged (4.97% = a 0.497% move).

Fitted presets:
| Preset | Bars | N | buf | SL | Match |
|---|---|---|---|---|---|
| v2.2.x BTCUSDT.P "45 min" | 45m | 180 | 0.6% | 6% | 5/5 entry prices exact to the cent; pending levels 43537.20, 51821.20 and 45803.85 also exact |
| v2.1.6 v.5 BTCUSDTPERP "15 min" stats | 45m | 210 | 0 | 6% | **50/50 timestamps exact, 50/50 peak-profit labels exact to 0.01%** (also with the Pine-equivalent port) |
| ETHUSDT stats (spot ticker) | 45m | ~450 | 0 | ~8% | 21/30 exact, 8 more within 1 day (spot vs perp data) |

- Even the "15 min" preset stamps all of its signals on 45m bar opens. The engine runs on 45m bars (request.security or a 45m chart).
- The "Fake LONG breakout" in the video was a misreading: the Binance high on 20 Jan 2022 was 43,495, which never reached the 43,537.20 level.
- TP ladders (fixed %). v2.2.3: 0.3 / 1 / 2 / 3 / 10%, with SL 6%. Short TPs = entry/(1+p). Predictum X: 1 / 2 / 3 / 4 / 8 / 20%, DCA at −7 / −15 / −25%, SL about −8%.
- "Get ready" alert = price within some % of the pending level. The exact % is not yet confirmed (OG Breakout default 0.5%).

## Reality check (BTC 45m N=210, close at SL or opposite signal, 1x, 0.08% fees, 2020-01 → 2022-03)
- 84 trades. TP2 hit on 88% (the advertised "accuracy"). Realised win rate 31%, average +1.7%/trade, 2.2x total, max drawdown 48%.
- N=180 + 0.6% buffer: 96 trades, 38% realised wins, 3.8x total, max DD 37%.
- ETH N=450: 40 trades, 38% realised wins, 2.2x total, max DD 41%.
- At the advertised 10x leverage these drawdowns would liquidate the account. The edge is plain trend-following. The 90%+ accuracy is the TP2 definition.

## Build: OG Breakout v1.0 (`indicator/og_breakout.pine`, Pine v6, 15 Oct 2026, not yet compiled in TradingView)
- Presets: BTC 180/0.6%/6%, BTC 210/0%/6%, ETH 450/0%/8%, Custom. Engine timeframe input (default 45). The chart timeframe must be ≤ the engine timeframe, otherwise a warning shows.
- Channel via request.security(..., [ta.highest(high,N)[1], ta.lowest(low,N)[1]], lookahead_on), so there is no repaint.
- TP ladders: Classic 0.3/1/2/3/10, Wide 1/2/3/4/8/20, or Custom. Optional DCA lines. Leverage for the labels.
- Chart: background by last signal, next-entry lines, TP/SL lines per trade, entry price/time label, peak-profit label, "Get ready" labels.
- Stats table: recent signals with the leveraged peak and the realised %. Summary: accuracy (TP# before stop), per-TP hit rates, realised win %, net and max DD (1x).
- Alerts: alert() for entry (with the TP/SL plan), each TP, the stop and get-ready, plus alertconditions for Long and Short.

## Product lineage
- Predictūm v2.1.5 → v2.4.2 (2021–2023), PRO New Era v1.1–1.5 (2023–2024, 50–63 presets, DCA+SL / No DCA+SL), Predictūm X (2025–26, Bybit 45m, TP1–6 + probability + strategy score).
- Crackōs = a clone. Best_Algos_Lab "Predictum" (2026) describes the same concept.

## Sources
- Screenshots and videos in `research/`.
- TradingView: Predictum PRO (https://in.tradingview.com/script/ikkuuaOI-Predictum-PRO) and Predictum by Best_Algos_Lab (https://www.tradingview.com/script/otjJfMRf-Predictum/).
- Telegram mirror: https://telemetr.io/en/channels/1456872361-predictum

## Data and code
- `tools/fetch_data.py` downloads Binance futures 15m CSVs into `data/` (git-ignored).
- `tools/fit_engine.py` holds the loader, the 45m resampler, the simulator and the raw ground-truth signal lists (BTC 50, ETH 30). Running it prints "BTC v.5 matched 50 / 50".
