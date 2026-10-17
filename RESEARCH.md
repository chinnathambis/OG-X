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

## Timeframe study (tools/tf_study.py, 12 coins, train 2024-10→2025-12, test 2026)
The same engine was run on 15m, 30m, 45m, 1h, 2h and 4h, with the channel length set in **days** (1–26, plus 30–60 on 1h/4h), buffer 0–1.5% and stop 3–10%.
- **The timeframe barely matters.** For the same number of days, the results on 15m … 4h are nearly identical. The top train pick is the same on every timeframe (26 days, 1.5% buffer, 4% stop): test median +14% to +15%, 10/12 coins up, median DD 21%. Averaged over each timeframe's top-10 train picks, the test median is +8% to +11%. 4h was marginally best, which is within noise.
- **What matters is how many days the channel covers.** The sweet spot is about 2–5 weeks (14–35 days). Below 10 days it whipsaws (negative train). Above 40 days there are too few trades and train turns negative.
- Universal (500 × 45m ≈ 15.6 days) and Very slow (850 × 45m ≈ 26.6 days) sit inside that sweet spot.
- So there is no need to tune a timeframe per preset. v1.5 defines presets in time and scales them to whatever timeframe is used. Practical gain: a **4h chart loads 2+ years in TradingView**, so the stats table covers ~30+ trades instead of 7–11 on 45m.
- Summary file: `research/tf_study_summary.csv`.

## Decision (15 Oct 2026): main indicator = original Predictum
The user chose to keep the main indicator as the faithful Predictum recreation (v2.0). The tuning work above (presets, exit study, timeframe study) is kept for reference, and v1.1–v1.5 stay in `indicator/archive/`.

## Predictum X check (15 Oct 2026, 14 signals from Telegram screenshots, Bybit 45m data)
Signals: ZEREBRO, GRIFFAIN, BANANA, GUN, GOAT, GPS, AVAAI, BERA, XCN, JELLYJELLY, DOOD, FARTCOIN, VANA, AVL (all longs, Oct 2025 – May 2026). List in `research/x/x_signals.csv`.
- **Timing:** every ID time is a 45m candle open, and the posted price lies inside that candle. Signals fire intrabar, like v2.
- **Same breakout engine, very likely.** 13 of 14 signal candles make a new high over the previous 4–38 days (typically 7–9 days ≈ 200–300 bars of 45m). **One setting, channel 200 bars + 0.8 % buffer, makes 12 of 14 signals a fresh breakout on exactly the signal candle** (no touch in the 8 candles before). By chance that would be expected for well under 1 in 14. The other two fit nearby per-coin settings (GUN 255 bars / 0.6 %, XCN 255–450 / 0.6 %). This is close to Predictum v2 BTC (180–210 bars, 0–0.6 %), so X looks like the same engine with per-coin presets.
- **The "current price" in the post is not the fill level:** e.g. GRIFFAIN's price is below the candle open. It's the market price at posting time, so the exact entry level can't be read from the post.
- **TPs and DCA:** TP = price × (1 + 1 / 2 / 3 / 4 / 8 / 20 %) plus ~0.05 %; DCA = price × (1 − 7 / 15 / 25 %).
- **Probability / PNL:** look like per-coin history (TP hit rate; total PNL if always closed at that TP, which can be negative).
- **Still unknown:** the stop rule, the per-coin N/buffer for each coin, and shorts (no short signals yet). Next: the full Telegram export (signals + "TP ✅ / stop" follow-ups), then fit per coin.

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

## Top-coin scan: original strategies on 40 coins (15 Oct 2026)
Binance futures 15m → 45m, Oct 2024 – Oct 2026, 1×, fees 0.08 %, exit at the stop or the next signal. Qualifies = profitable in both 2024–25 and 2026. Full table: `research/orig_strategies_top_coins.csv`.
- 14 of 40 coins qualify on at least one strategy. The best per coin: ZEC (BTC v.5) +1244 %, DOGE (ETH) +328 %, ARB (v2.2) +180 % ⚠, SUI (ETH) +171 % ⚠, QNT (ETH) +143 %, ETH (ETH) +141 %, UNI (v2.2) +117 % ⚠, 1000PEPE (v.5) +110 %, XRP (ETH) +101 %, AAVE (ETH) +100 %, SOL (v.5) +49 %, PAXG (v2.2) +36 % (DD 11 %).
- AKE (+1385 %) and PUMP are too new to trust (listed 2025).
- The ETH strategy (450 bars) carries most of the winners; the slow channel suits trending alts. BTC itself still doesn't qualify on any of the three.

## Data point: Predictum PRO "New Era" (screenshot, 16 Oct 2026)
- Legend: "Predictūm PRO | New Era v.1.1.1 No DCA + SL 20 20 TP 5", on a **30 min** chart. This is a different product line from the 45-min strategies.
- Its warning box checks four things: timeframe 30 min, a supported ticker, BINANCE exchange, and a ticker ending in ".P".
- It shows a long list of supported tickers for the "No DCA + SL" type. Visible part: 1000SHIB, 1INCH, ALICE, ALPHA, API3, ARPA, ATA, ATOM, AXS, BAKE, BAND, BEL, CHZ, COMP, COTI, CRV, DASH, DENT, DOT, DUSK, DYDX, ENJ, FIL, FLOW, GRT … So it runs per-coin settings for many alts.
- The name suggests parameters "20 20 TP 5". These are unknown; possibly SL 20 % / 20 bars / 5 TPs. Not researched.

## Per-coin tuning with a 2026 test (16 Oct 2026)
- **Setup:** the same engine and TP ladder. Each coin's bars (60–700), buffer (0–1 %) and stop (3–10 %) are picked on **Oct 2024 – Dec 2025 only**, by net ÷ drawdown with a neighbour-robustness check. The pick is then tested on **2026**, which tuning never saw. Binance futures 45m, 1×, fees 0.08 %. Full table: `research/per_coin_tune_2026_test.csv`.
- **Pass rule:** profitable in training; 2026 profit with ≥ 8 trades; 2026 PF ≥ 1.2; 2026 drawdown ≤ 50 %; history from before Apr 2025.
- **14 of 40 pass:** ZEC, ZEREBRO, ARB, STRK, WLD, UNI, TAO, SOL, EGLD, AAVE, SUI, BTC, ETH, DOGE.
  - New coins that were not presets: STRK, WLD, TAO and EGLD (few trades). ZEREBRO and BTC only scraped through training (+4 %, +6 %), so treat them as luck.
- **Tuning is not always better.** Tuned XRP, 1000PEPE, QNT and PAXG failed in 2026, while their original-strategy presets passed. The original strategies are the more robust choice where they already work.
- **The tuned settings fix the weak ⚠ presets:** SUI (2026 +1 % → +26 %), ARB (2024–25 +1 % → +574 %) and UNI (DD 66 % → 31–38 %).

## Preset scan round 2: 125 more coins (16 Oct 2026)
- **Coins:** the top 150 by volume minus round 1, plus Predictum's "New Era" alts; 125 downloaded, 90 with data from before Apr 2025. Data: `data/*.csv.gz`. Results: `research/orig_strategies_round2.csv`, `research/per_coin_tune_round2.csv`.
- **Original strategies, quality rule** (both periods ≥ +10 %, DD ≤ 60 %, PF ≥ 1.3): PENGU, MINA, DASH, 1000BONK, RAYSOL, AERO, SEI, BOME, BLUR, POL, KMNO, GRT, ENJ, GALA, RENDER.
  - VVV is +1001 % but DD 64 % (⚠).
  - Rejected: EPIC (2024–25 +2 %), ATOM (+4 %), DOT (2026 +8 %), LSK (DD 77 %), CHZ (DD 64 %).
- **Per-coin tuning** (tuned on 2024–25, 2026 test, same pass rule as round 1, training ≥ +20 %): 22 pass.
  - New coins only via tuning: S (+333 % in 2026, DD 21 %), XLM, KAIA, AR (8 test trades), TRX (10 test trades).
  - SAND: tuned 660 / 1 % / 8 % (2026 +23 %, DD 22 %) instead of the original v2.2 (DD 67 %).

## Predictum X: full Telegram export (17 Oct 2026)
Source: the public channel export (`ChatExport_2026-10-17`, Apr 2020 – May 2026), parsed with `tools/parse_telegram_export.py`. Predictum X era: **31 signals, 12 Oct 2025 – 25 May 2026**, all Bybit 45m, 30 Longs + 1 Short (`research/x/x_signals_full.csv`). Bybit 15m data: 30 coins (SERAPH has no Bybit data; FORTH's data starts after its signal).
- **Signal format is fixed.** TPs = +1 / 2 / 3 / 4 / 8 / 20 % from the current price on every signal. DCA = −7 / −15 / −25 % on every Long. The Short's stop is +8 % ("SL … or DCA"). Channel "Profit +10 % … +200 %" = those TPs at 10×.
- **The channel only posts wins.** Every follow-up is "TP x ✅"; no stop or loss is reported in 7 months.
- **Engine: confirmed the same channel breakout.** One setting, **200 bars + 0.9 % buffer**, fires a fresh breakout (no touch in the 8 candles before) on exactly the signal candle for **23 of 29** checkable signals. A random candle passes this test 0.55 % of the time, so chance would give about 0.2 matches. 200 bars / 0.6–0.8 % gives 22. Misses: TAO (fits 220–240 bars), ACE (310–390, and 200/0.9 fires one candle earlier), FLR, XCN (250–450), GUN (90–250, 0 % buffer), and MUBARAK (12 Oct 2025, a rebound after the 10 Oct crash, not a breakout).
- **Real outcomes (30 days after each signal, 1×, no fees; `research/x/x_outcomes_full.csv`, `tools/x_outcomes.py`), 29 signals:**

  | | TP1 | TP2 | TP3 | TP4 | TP5 | TP6 |
  |---|---|---|---|---|---|---|
  | Reached at some point | 29 | 27 | 25 | 24 | 21 | 12 |
  | Reached before a −8 % drop | 26 | 24 | 22 | 18 | 13 | 5 |

  - 27 of 29 fell 8 % below entry at some point within 30 days, and 21 of 29 fell past DCA3 (−25 %). Median peak +15 %, median worst −32 %.
  - With an 8 % stop: 1/6 at each TP → −0.6 % per trade on average (13/29 profitable). All out at TP1 → +2 % in total over 29 trades. All out at TP4 → −16 %. All out at TP5 → −24 %.
  - **"Strategy score" does not predict anything:** rank correlation with the peak 0.05, with TPs before −8 % 0.01. Score ≥ 10: median peak +24 %, 3.6 TPs; score < 10: +12 %, 3.8 TPs.
- **Conclusion.** Predictum X is the same 45m channel-breakout engine as Predictum v2 / OG X, run on small Bybit coins with a ~200-bar channel and a tight TP ladder. Its posted "accuracy" comes from TP1 at +1 % (almost always touched) and from only posting wins. The real edge on these signals, as traded with its own TPs, is about zero. OG X's own presets (hold to stop or next signal, tested per coin) are the better use of the engine.
