# OG Breakout — build queue

**How we work (agreed 15 Oct 2026):** questions get answers. Any fix or feature that comes out of them is added here with a priority, and nothing is built until the user says "build". Then everything queued is built in one go as one version. Full feature list: `FEATURES.md`. Released changes: `indicator/VERSIONS.md`.

**Priorities**
- **P0:** bug or wrong output. Build first.
- **P1:** agreed feature.
- **P2:** idea, not decided yet. Needs a yes before it moves up.

Current release: **v2.2** (the TP-labels-on-the-entry-candle fix shipped before this way of working was agreed).

## P0: bugs
1. **Header tag overlaps TradingView's symbol line → do it the Predictum way** (reported 15 Oct 2026; Predictum screenshot: "Predictūm v.2.3.7 BTCUSDT.P - Binance Futures | 45 min timeframe" shown as the indicator's own line in TradingView's legend, directly under the symbol line, inside the normal legend box).
   - Remove the top-left header table (it prints over TradingView's symbol line).
   - Use TradingView's legend (status line) instead. Set the indicator short title to "OG Breakout v2.x". Show only the Strategy input in the status line (`display = display.status_line`) and hide every other input (`display = display.none`), so the legend reads like "OG Breakout v2.3 BTCUSDT.P - Binance Futures | 45 min timeframe".
   - Name the Strategy options in that same format, e.g. "BTCUSDT.P - Binance Futures | 45 min timeframe" (v2.2), "BTCUSDT.P - Binance Futures | 45 min timeframe | v.5", "ETHUSDT.P - Binance Futures | 45 min timeframe", plus the coin presets (P1 #3). With Auto, the legend can only show "Auto", because inputs can't change themselves. Check in TradingView whether Auto should stay the default, or whether the coin's own option should be picked by hand so the legend shows the coin.
   - No extra text on the chart.
2. **Helper: big "+" on the upcoming trade, like Predictum** (requested 15 Oct 2026; Predictum v2.1.5 CHZ screenshot).
   - Draw a large "+" cross a few bars to the right of the last candle, at the next entry price: green for the next Long, red for the next Short. Show both when both are possible.
   - A blue callout tag with the entry price (e.g. "0.37869") points at the "+" from above and to the right. This replaces the current plain blue price tag.
   - "Get ready to Long": a blue ↑ arrow under the candle with grey text "Get ready to Long" below it, no box; mirrored for Short (red ↓ above the candle). A small blue ▶ marker on the candle where the alert fired.
   - Redrawn on the last bar only, so it never piles up on history. Shown when "Show Helper" is on.

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
  - **Data point 1 (screenshot, 15 Oct 2026):** AVLUSDT, Bybit, 45m. "Open Long" alert 24 Oct 2025, ID `Long_AVL_24_10_2025_06_45`, current price 0.1313, strategy score 10.72. TP1–6 = 0.13264 / 0.13401 / 0.13527 / 0.13667 / 0.14189 / 0.15766 (+1 / 2 / 3 / 4 / 8 / 20 % from ≈0.13132). DCA 0.12211 / 0.1116 / 0.098475 (−7 / −15 / −25 %). Probabilities 100 / 96 / 88 / 88 / 63 / 33 %. Chart also shows a Long ≈30 Sep 2025 and a Short ≈9 Oct 2025. To test the engine, download Bybit AVLUSDT 45m (Sep–Nov 2025) and check whether a channel breakout fires at those times.
- **Predictum X look (option)** (from the same screenshot): "Long ↗" / "Short ↘" boxes, monospace green "Peak profit" boxes, teal/pink background, TP1–4 lines close together with TP5 and TP6 further out, red SL line.
- **Predictum X–style alert message** (from the same screenshot): "#COIN | Open Long · Current price · Settings: EXCHANGE. Timeframe: 45 min · Strategy score · TP1–6 with Probability % · DCA 1–3 · ID: #Long_COIN_dd_MM_yyyy_HH_mm". Probability per TP can come from our own statistics (the TP hit rate on this coin). "PNL %" and "Strategy score" formulas are unknown (PNL doesn't scale with the TP distance), so leave them out until the X research explains them.
- **One alert for all coins** (hub, Telegram-ready messages), like `og_shot_hub.pine`.
- **Re-check on the full history** (`tools/fetch_max_data.py`, 24 coins from 2019) before trading real money.
- **"Experimental" strategy group** for settings that only look good on recent months (e.g. EGLD 15m 500 / 0.4 % / 8 %), clearly marked as not validated.

## Dropped
- **Move the stop to entry after +3 %** (15 Oct 2026): Predictum's take-profits are tight (0.3 / 1 / 2 / 3 %), so +3 % is already TP4. A breakeven stop there would cut trades inside the TP ladder.
