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

## Preset tuning 2024–2026 (12 coins, Binance futures, 45m)
Grid: N 60–1000, buffer 0–1.5%, stop 3–10% (900 combos × 12 coins). Realised model: exit at the stop or the next signal's entry, 0.08% fees, 1x. Train Oct 2024 – Dec 2025, test Jan – Oct 2026 (never seen while picking).
- **Per-coin best picks overfit.** Their 2026 tests were flat or negative on ADA, AVAX, HYPE, XRP and LINK, and most picks sat on the grid's edges with ~15 trades.
- **One universal setting holds up: N 500, buffer 0.6%, stop 3%.** It ranked top by median train score across coins. In the 2026 test, 10 of 12 coins finished positive: median +42%, median max DD 26%, PF 1.3–3.0, win rate 13–35% (small 3% losses, large trend winners). Neighbours (N 450–550, buffer 0.3–1%, stop 3–4%) behave the same, so this is not a lucky spike.
- Universal 2026 test per coin: ETH +74%, DOGE +73%, SUI +79%, BNB +47%, XRP +43%, BTC +42%, AVAX +42%, SOL +28%, LINK +13%, ADA +3%, HYPE −21%, TAO −22%. HYPE and TAO also lost in training, so they are excluded.
- The original Predictum BTC setting (180 / 0.6% / 6%) had a negative median train score in 2024–2025: the market favours longer channels and tighter stops now.
- Files: `research/tune_grid_2024_2026.csv` (every combo), `research/universal_500_per_coin.csv`, `tools/tune_presets.py`, `tools/grid_all.py`, `tools/fetch_presets_data.py`.
- OG Breakout v1.2: "Universal · 500 · 0.6% · 3%" is the default preset. The stats header shows "✓ validated" or "⚠ not validated on this coin". Realised stats now deduct fees (input, default 0.08%).

### Preset list (OG Breakout v1.4, corrected short-trade maths)
Bug fixed in v1.4: the tuner scored a short closed on a flip as entry/exit − 1 instead of 1 − exit/entry, which overstated winning shorts. The indicator itself was always right. Numbers below are after the fix.
Test = Jan–Oct 2026 (unseen). Median across 12 coins. "Both" = coins profitable in train and test (the coins the header marks ✓).
| Preset | Test median | Coins + in test | Median max DD | Trades/yr/coin | Both |
|---|---|---|---|---|---|
| Universal · 500 · 0.6% · 3% | +27% | 9/12 | 26% | ~27 | AVAX DOGE ETH LINK SUI XRP |
| Fast · 60 · 0% · 10% | +23% | 9/12 | 33% | ~124 | ADA DOGE ETH SUI TAO XRP |
| Active · 240 · 0% · 4% | +7% | 7/12 | 32% | ~39 | ETH HYPE SOL XRP |
| Medium · 340 · 0% · 3% | +10% | 9/12 | 33% | ~37 | AVAX DOGE ETH XRP |
| Swing · 450 · 1% · 3% | +21% | 9/12 | 30% | ~32 | AVAX DOGE ETH SUI XRP |
| Swing · 550 · 0% · 4% | +9% | 8/12 | 23% | ~22 | AVAX DOGE ETH SUI XRP |
| Slow · 600 · 0.6% · 3% | +3% | 7/12 | 26% | ~27 | DOGE ETH SUI XRP |
| Slow · 800 · 1% · 3% | +15% | 10/12 | 20% | ~22 | AVAX DOGE ETH LINK SUI XRP |
| Very slow · 850 · 1.5% · 4% | +13% | 11/12 | 21% | ~16 | AVAX BTC DOGE ETH LINK SOL SUI XRP |
Coin-tuned, train → test: BTC 700/1%/3% +6% → +25%; ETH 700/0.6%/3% +198% → +18%; DOGE 640/0%/4% +277% → +13%; SUI 700/1%/4% +338% → +26%. SOL 220/1%/8% (+91% → −3%) was removed.

## Exit study (tools/exit_study.py, 12 coins, same train/test split)
Entry engine unchanged; only the exit changes. Compared with "hold to the stop or the opposite signal":
- **Scale-out 20% at each of 1/2/3/4/8%** first looked best (12/12 coins up), but most of that came from re-entering on the same bar the last target filled, at a price already passed. With same-bar re-entry blocked it is worse than holding (Universal test +5% vs +27%). Rejected.
- **Scale-out 10/10/10/20/20 (40% rides to the stop or flip):** roughly halves the drawdown (Universal train 37% → 18%, test 26% → 13%) but also halves the return (test +11% vs +27%). A smoother, lower-return option.
- **Breakeven after +3%:** helps the slower presets (Slow 800: better risk-adjusted on 9/12 coins in both periods, test DD 20% → 13%; Swing 450: 7–8/12). Neutral for Universal, worse for Fast.
- **Breakeven after +1% or +2%:** cuts winners too early. Not better.
- **Trailing stops (5/8/12%):** mixed. 8% is about neutral; 5% hurts.
- **Trend filter (only trade with a 3× longer channel's midline):** good 2026 test but poor 2024–25 train. Inconsistent, rejected.
- Conclusion: the original hold-to-stop/flip exit is already close to the best. Breakeven after +3% is worth offering for the slower presets, and scale-out 10/10/10/20/20 for a smoother ride.

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
