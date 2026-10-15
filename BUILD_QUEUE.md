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
3. **Predictum X–style trade background, light and dark (moved up from P1 on 15 Oct 2026; VANA and GPS light screenshots, API3 dark screenshot `research/x/x_dark_api3.png`).**
   - The trade's shading starts at the stop line and runs to the chart edge on the profit side, instead of covering the full chart height. Long: from SL up to the top (teal). Short: from SL down to the bottom (pink). Nothing is shaded on the far side of the stop.
   - It runs from the entry candle to the exit candle, with the red SL line along its edge.
   - New input under "Highlight the background": style "SL to edge (Predictum X)" (default) or "Full height (Predictum)".
   - Works in both themes, following the existing "Light theme" switch. Light: teal #5e9fa3 / pink #f48fb1 at ~55 % transparency (X look). Dark (match the API3 X screenshot): deep teal box (≈ #26a69a at ~85 % transparency) for longs and deep maroon (≈ #f23645 at ~80 % transparency) for shorts, so candles and TP lines stay readable.
   - Mocks: `research/x_background_mock.png` (light), `research/x_background_mock_dark.png` (dark).
   - Build note: draw it as a box from the SL to a far price. Check in TradingView that the far edge doesn't squash the price scale. If it does, cap the box at the highest high (Long) or lowest low (Short) of the visible trade plus a margin.

## P1: agreed features
1. **Next-signal exit stub on the current trade (Mock B, agreed 15 Oct 2026).** Under "Show SL/TP of the current position":
   - No trailing line and no history. On the last bar only, draw the next opposite signal as a short dashed stub starting ~2 bars right of the live candle, with a "+" at the level (red for a Short flip, green for a Long flip).
   - The closer exit (fixed stop or next signal) is bold and tagged "◀ EXIT" with the % result if it hits, e.g. "◀ EXIT Next signal (Short) 2,757 +7.3%". The other one is dimmed and still shows its %.
   - The fixed stop stays the normal red position line. It turns thin and dim once the next signal is closer.
   - Display only: the stop logic already ends a trade at whichever comes first. Mock: `research/effective_stop_mock_B.png` (trailing-line version rejected).
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
- **Predictum X research (next step after the 2021–22 recreation).** _Status 15 Oct 2026: 14 signals checked. Same breakout engine very likely (one setting, 200 bars + 0.8 %, matches 12/14 signal candles exactly; see RESEARCH.md). Waiting for the full Telegram export (shorts and TP/stop follow-ups) to recover per-coin settings and the stop rule._ Collect 10–20 real Predictum X signals with exact time, coin, entry and TPs (Telegram posts or screenshots). Check whether X uses the same channel-breakout engine, and recover its per-coin settings, TP1–6, DCA sizing and stop. Then decide whether to add X-style strategies.
  - **Data point 1 (screenshot, 15 Oct 2026):** AVLUSDT, Bybit, 45m. "Open Long" alert 24 Oct 2025, ID `Long_AVL_24_10_2025_06_45`, current price 0.1313, strategy score 10.72. TP1–6 = 0.13264 / 0.13401 / 0.13527 / 0.13667 / 0.14189 / 0.15766 (+1 / 2 / 3 / 4 / 8 / 20 % from ≈0.13132). DCA 0.12211 / 0.1116 / 0.098475 (−7 / −15 / −25 %). Probabilities 100 / 96 / 88 / 88 / 63 / 33 %. Chart also shows a Long ≈30 Sep 2025 and a Short ≈9 Oct 2025. To test the engine, download Bybit AVLUSDT 45m (Sep–Nov 2025) and check whether a channel breakout fires at those times.
  - **Data point 2 (dark screenshot, 15 Oct 2026):** API3USDT, Bybit, 45m, Long on Sat 16 Aug 2025 11:15 (chart time zone unknown), peak profit +1193.06 %. The indicator's legend reads "Crackōs v.1.0.1 + Alerts", which is probably the TradingView name of Predictum X.
- **Predictum X look (option)** (from the AVL screenshot; API3 dark screenshot adds: blue "Prepare to Long" box on the candle before entry, white dashed vertical line at the entry candle, white dashed entry-price line running to the right edge, "Long ↗" label drawn in red): "Long ↗" / "Short ↘" boxes, monospace green "Peak profit" boxes, teal/pink background, TP1–4 lines close together with TP5 and TP6 further out, red SL line.
- **Predictum X–style alert message** (from the same screenshot): "#COIN | Open Long · Current price · Settings: EXCHANGE. Timeframe: 45 min · Strategy score · TP1–6 with Probability % · DCA 1–3 · ID: #Long_COIN_dd_MM_yyyy_HH_mm". Probability per TP can come from our own statistics (the TP hit rate on this coin). "PNL %" and "Strategy score" formulas are unknown (PNL doesn't scale with the TP distance), so leave them out until the X research explains them.
- **One alert for all coins** (hub, Telegram-ready messages), like `og_shot_hub.pine`.
- **Re-check on the full history** (`tools/fetch_max_data.py`, 24 coins from 2019) before trading real money.
- **"Experimental" strategy group** for settings that only look good on recent months (e.g. EGLD 15m 500 / 0.4 % / 8 %), clearly marked as not validated.

## Dropped
- **Move the stop to entry after +3 %** (15 Oct 2026): Predictum's take-profits are tight (0.3 / 1 / 2 / 3 %), so +3 % is already TP4. A breakeven stop there would cut trades inside the TP ladder.
