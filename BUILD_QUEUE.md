# OG Breakout — build queue

**How we work (agreed 15 Oct 2026):** questions get answers. Any fix or feature that comes out of them is added here with a priority, and nothing is built until the user says "build". Then everything queued is built in one go as one version. Full feature list: `FEATURES.md`. Released changes: `indicator/VERSIONS.md`.

**Priorities**
- **P0:** bug or wrong output. Build first.
- **P1:** agreed feature.
- **P2:** idea, not decided yet. Needs a yes before it moves up.

Current release: **v2.2** (the TP-labels-on-the-entry-candle fix shipped before this way of working was agreed).

## P0: bugs
1. **Header tag overlaps TradingView's symbol line** (reported 15 Oct 2026, XPLUSDT.P 30m). The tag "OG Breakout v2.2 XPLUSDT.P - BINANCE Futures | 45 min timeframe | Custom" sits in the top-left corner, under TradingView's own symbol/OHLC line, so the two texts print over each other. Fix: move the tag to the bottom-left corner, and add a "Show header tag" switch (Helper settings, default on). Keep it on one short line.

## P1: agreed features
1. **Next-signal line on the current trade.** Under "Show SL/TP of the current position", draw the next opposite signal as a dashed trailing line next to the fixed stop, and label whichever is closer "effective stop". Display only: the stop logic already ends a trade at whichever comes first. Mock: `research/stop_mock.png`.
2. **Strategy type "SL" / "DCA + SL"** (Predictum PRO).
   - Enter with ¼, add ¼ at −7 / −15 / −25 %. TPs are counted from the average price. The final stop sits 8 % beyond the last level. The trade is held until the opposite signal or the stop.
   - Stats: full-capital results, averaging buys used per trade, and the worst-case loss (~22 % of capital).
   - Tooltip: low leverage only (1–2×).
   - Backtest Oct 2024 – Oct 2026: ETH 450 +42 % (DD 11 %) vs fixed stop +141 % (DD 29 %); BTC 210 +2 % (DD 12 %) vs −23 % (DD 42 %).

3. **Coin presets using the original Predictum strategies** (added 15 Oct 2026). Add a Strategy menu entry per qualifying coin; Auto picks it on that coin. A coin qualifies only if the strategy made money in both 2024–25 and 2026 (Binance futures, 45m, 1×, fees). From the first 13 coins:
   - DOGEUSDT.P | 45 min (ETH strategy 450 / 0 % / 8 %): +328 % (2024–25 +249 %, 2026 +23 %), DD 45 %
   - ETHUSDT.P | 45 min (ETH strategy, already in): +141 % (+49 %, +62 %), DD 29 %
   - XRPUSDT.P | 45 min (ETH strategy): +101 % (+77 %, +13 %), DD 62 %
   - SUIUSDT.P | 45 min (ETH strategy): +171 % (+168 %, +1 %), DD 45 %. Weak in 2026: mark ⚠
   - SOLUSDT.P | 45 min (BTC v.5 strategy 210 / 0 % / 6 %): +49 % (+25 %, +20 %), DD 45 %
   - Did not qualify: BTC, BNB, ADA, LINK, AVAX, HYPE, TAO, EGLD.
   - Pending: the top-50 scan (`tools/fetch_top_coins.py`), then add any further qualifiers.

## P2: ideas
- **Predictum X research (next step after the 2021–22 recreation).** Collect 10–20 real Predictum X signals with exact time, coin, entry and TPs (Telegram posts or screenshots). Check whether X uses the same channel-breakout engine, and recover its per-coin settings, TP1–6, DCA sizing and stop. Then decide whether to add X-style strategies.
- **One alert for all coins** (hub, Telegram-ready messages), like `og_shot_hub.pine`.
- **Re-check on the full history** (`tools/fetch_max_data.py`, 24 coins from 2019) before trading real money.
- **"Experimental" strategy group** for settings that only look good on recent months (e.g. EGLD 15m 500 / 0.4 % / 8 %), clearly marked as not validated.

## Dropped
- **Move the stop to entry after +3 %** (15 Oct 2026): Predictum's take-profits are tight (0.3 / 1 / 2 / 3 %), so +3 % is already TP4. A breakeven stop there would cut trades inside the TP ladder.
