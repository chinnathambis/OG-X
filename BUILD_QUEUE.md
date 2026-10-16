# OG Breakout — build queue

**How we work (agreed 15 Oct 2026):** questions get answers. Any fix or feature that comes out of them is added here with a priority, and nothing is built until the user says "build". Then everything queued is built in one go as one version. Full feature list: `FEATURES.md`. Released changes: `indicator/VERSIONS.md`.

**Priorities**
- **P0:** bug or wrong output. Build first.
- **P1:** agreed feature.
- **P2:** idea, not decided yet. Needs a yes before it moves up.

Current release: **OG X v.2.4.3 + Alerts** (16 Oct 2026). Next build: P1.

## P0: bugs and fixes for v.2.4.4
1. **Chart check, like Predictum's warning but showing what is wrong** (approved 16 Oct 2026; mock `research/mocks/approved/v243_chart_check.png`).
   - **Red WARNING box** when the chart differs from the presets. Each check gets ✅ or ❌:
     - timeframe 45 min or lower
     - a supported ticker (a preset exists)
     - exchange is BINANCE (or BYBIT); the ❌ line names the actual exchange
     - ticker ends with ".P" (perpetual futures)
     - plus the note "Signals still run with Custom settings; results may differ from the presets."
   - **Blue "SUPPORTED TICKERS (presets)" list** under the box: BTCUSDT.P (v2.2 and v.5), ETH, ZEC, DOGE, QNT, 1000PEPE, XRP, AAVE, SOL, PAXG, SUI ⚠, UNI ⚠, ARB ⚠, with the footer "Binance futures · 45 min · other coins: Custom".
   - **Correct chart but no preset** (e.g. LINKUSDT.P with Auto): no red box. A blue info line "ℹ No preset for X — Custom settings are in use (N bars · buf % · stop %)" with ✅ timeframe · ✅ exchange · ✅ ".P", and the supported list under it.
   - Signals keep running in both cases (unlike Predictum, which blocks).
   - New setting **"Hide the chart check"** turns both boxes off.

2. **Add BCHUSDT.P preset** (requested 16 Oct 2026). Menu entry "BCHUSDT.P - Binance Futures | 45 min timeframe", picked by Auto on BCH, using the **BTC v.5 strategy** (210 / 0 % / 6 %). Mark it **⚠** in the tooltip and the stats ("⚠ BCH preset: lost money in 2024–25") and add it to the chart-check ticker list with ⚠.
   - Backtest (Binance futures 45m, 1×, fees): it lost money overall on all three strategies. BTC v.5 −50 % total (2024–25 −74 %, 2026 +93 %, DD 78 %, PF 0.89). ETH −41 % (−57 %, +37 %, DD 70 %). v2.2 −61 % (−74 %, +47 %, DD 88 %). v.5 was picked for the strongest 2026.

## P1: agreed features
1. **Strategy type "SL" / "DCA + SL"** (Predictum PRO).
   - Enter with ¼, add ¼ at −7 / −15 / −25 %. TPs are counted from the average price. The final stop sits 8 % beyond the last level. The trade is held until the opposite signal or the stop.
   - Stats: full-capital results, averaging buys used per trade, and the worst-case loss (~22 % of capital).
   - Tooltip: low leverage only (1–2×).
   - Backtest Oct 2024 – Oct 2026: ETH 450 +42 % (DD 11 %) vs fixed stop +141 % (DD 29 %); BTC 210 +2 % (DD 12 %) vs −23 % (DD 42 %).

## P2: ideas
- **Northline bot alerts, same as OG Shot (parked 16 Oct 2026).** Send OG Shot's JSON so the Northline bot / mini app can trade OG X signals.
  - New trade: `{"event":"LONG/SHORT","symbol","exchange","tf":"45m","strategy":"OG X <COIN>","entry","zone":[lo,hi],"tp":[TP1–TP4],"sl","accuracy":{all,short,long,last5,last10,last20},"time"}`.
  - Follow-ups: `TARGET` (targets hit) and `STOP`.
  - Plus a "Message format" setting (Telegram / JSON / Both) like OG Shot.
  - Draft defaults:
    - TP1–TP4 (+0.3 / 1 / 2 / 3 %) go to the bot; TP5 stays on the chart only.
    - Entry zone = entry → TP1.
    - The alert fires on the touch (intrabar), not at bar close.
  - Open points:
    - TP1 at +0.3 % with the bot's 50 % first close.
    - Check `CONTRACT.md` in the bot repo for allowed strategy names / fields.
    - One alert per chart (12) until the hub exists.
- **Predictum X research (next step after the 2021–22 recreation).** _Status 15 Oct 2026: 14 signals checked. Same breakout engine very likely (one setting, 200 bars + 0.8 %, matches 12/14 signal candles exactly; see RESEARCH.md). Waiting for the full Telegram export (shorts and TP/stop follow-ups) to recover per-coin settings and the stop rule._ Collect 10–20 real Predictum X signals with exact time, coin, entry and TPs (Telegram posts or screenshots). Check whether X uses the same channel-breakout engine, and recover its per-coin settings, TP1–6, DCA sizing and stop. Then decide whether to add X-style strategies.
  - **Data point 1 (screenshot, 15 Oct 2026):** AVLUSDT, Bybit, 45m. "Open Long" alert 24 Oct 2025, ID `Long_AVL_24_10_2025_06_45`, current price 0.1313, strategy score 10.72. TP1–6 = 0.13264 / 0.13401 / 0.13527 / 0.13667 / 0.14189 / 0.15766 (+1 / 2 / 3 / 4 / 8 / 20 % from ≈0.13132). DCA 0.12211 / 0.1116 / 0.098475 (−7 / −15 / −25 %). Probabilities 100 / 96 / 88 / 88 / 63 / 33 %. Chart also shows a Long ≈30 Sep 2025 and a Short ≈9 Oct 2025. To test the engine, download Bybit AVLUSDT 45m (Sep–Nov 2025) and check whether a channel breakout fires at those times.
  - **Data point 2 (dark screenshot, 15 Oct 2026):** API3USDT, Bybit, 45m, Long on Sat 16 Aug 2025 11:15 (chart time zone unknown), peak profit +1193.06 %. The indicator's legend reads "Crackōs v.1.0.1 + Alerts", which is probably the TradingView name of Predictum X.
- **Predictum X look (option)** (from the AVL screenshot; API3 dark screenshot adds: blue "Prepare to Long" box on the candle before entry, white dashed vertical line at the entry candle, white dashed entry-price line running to the right edge, "Long ↗" label drawn in red): "Long ↗" / "Short ↘" boxes, monospace green "Peak profit" boxes, teal/pink background, TP1–4 lines close together with TP5 and TP6 further out, red SL line.
- **Predictum X–style alert message** (from the same screenshot): "#COIN | Open Long · Current price · Settings: EXCHANGE. Timeframe: 45 min · Strategy score · TP1–6 with Probability % · DCA 1–3 · ID: #Long_COIN_dd_MM_yyyy_HH_mm". Probability per TP can come from our own statistics (the TP hit rate on this coin). "PNL %" and "Strategy score" formulas are unknown (PNL doesn't scale with the TP distance), so leave them out until the X research explains them.
- **One alert for all coins** (hub, Telegram-ready messages), like `og_shot_hub.pine`.
- **Re-check on the full history** (`tools/fetch_max_data.py`, 24 coins from 2019) before trading real money.
- **"Experimental" strategy group** for settings that only look good on recent months (e.g. EGLD 15m 500 / 0.4 % / 8 %), clearly marked as not validated.

## Shipped in v.2.4.0 (16 Oct 2026) (from v2.3 testing, 15–16 Oct 2026; mocks in `research/mocks/approved/v24_*`)
1. **Statistics table: keep the Predictum style, fix the layout (option A).** Same green centred block and emojis. Wrap the long last lines onto two lines (e.g. "Realised (stop or next signal, 1×, fees 0.08%):" / "wins … · net … · max DD …", and the two ACCURACY lines) so nothing runs over the chart or the price scale. No "Modern" style.
2. **TP levels: no tags on the chart (option B).** Remove the "TP1 ✓" chips. Expose TP1–TP5 and SL of the current trade as plots titled "TP1" … "TP5" and "SL" (scale only, not in the legend), so TradingView's own price-scale setting "Indicators and financials → name and value labels" shows them. Nothing custom drawn on the scale.
3. **When there is no open trade (after a stop): show only the closer "+" (option 2).** One "+" and one blue tag "Next Long at X / +x% from price" (or Short). The other side appears when price gets closer than the first. Fixes the two identical blue price tags.
4. **"Get ready" tag: blue pill with a triangle only.** "▲ Get ready" under the candle for a Long, "▼ Get ready" above the candle for a Short, blue, same size as the other tags. No arrow, no grey text, no dashed line, no ▶ marker.
5. **New name: "OG X v.2.4.0 + Alerts"** (chosen 16 Oct 2026). indicator() title and short title "OG X v.2.4.0 + Alerts"; legend reads e.g. "OG X v.2.4.0 + Alerts ZECUSDT.P - Binance Futures | 45 min timeframe". Versions from now on in this style (v.2.4.0, v.2.4.1 …). Update the header comment, alerts text ("OG X: LONG on …"), stats header and docs. Remove "recreation" wording from code comments and setting names. Mock: `research/mocks/approved/v24_name_format.png`.
6. **Bug: "⚠ UNI preset" note shown on a 1000PEPEUSDT.P chart** (v2.3 screenshot). Check how the preset is picked with Auto and fix.
7. **Legend shows only the name, not the Strategy** (no code change; user to check the two TradingView settings). Ask the user to check Chart settings → Status line → "Indicator arguments" and the indicator's Style → "Inputs in status line". If both are on and it still doesn't show, mock a fallback.

**Also shipped (approved 16 Oct 2026):** solid TP lines as thick as the SL line, the big "+" drawn as a cross, one tag size for all tags (only Long/Short small), SL/TP lines ending with the trade (same range as the background).

## Shipped in v2.3 (15 Oct 2026)
Kept as the build record. Approved mocks: `research/mocks/README.md`.

1. **Header tag overlaps TradingView's symbol line → do it the Predictum way** (reported 15 Oct 2026; Predictum screenshot: "Predictūm v.2.3.7 BTCUSDT.P - Binance Futures | 45 min timeframe" shown as the indicator's own line in TradingView's legend, directly under the symbol line, inside the normal legend box).
   - Remove the top-left header table (it prints over TradingView's symbol line).
   - Use TradingView's legend (status line) instead. Set the indicator short title to "OG Breakout v2.x". Show only the Strategy input in the status line (`display = display.status_line`) and hide every other input (`display = display.none`), so the legend reads like "OG Breakout v2.3 BTCUSDT.P - Binance Futures | 45 min timeframe".
   - Name the Strategy options in that same format, e.g. "BTCUSDT.P - Binance Futures | 45 min timeframe" (v2.2), "BTCUSDT.P - Binance Futures | 45 min timeframe | v.5", "ETHUSDT.P - Binance Futures | 45 min timeframe", plus the coin presets (P0 #4). With Auto, the legend can only show "Auto", because inputs can't change themselves. Check in TradingView whether Auto should stay the default, or whether the coin's own option should be picked by hand so the legend shows the coin.
   - No extra text on the chart.
2. **Helper: big "+" on the upcoming trade, like Predictum** (requested 15 Oct 2026; Predictum v2.1.5 CHZ screenshot).
   - Draw a normal-size "+" cross (not oversized, per 15 Oct 2026 feedback) a few bars to the right of the last candle, at the next entry price: green for the next Long, red for the next Short. Show both when both are possible.
   - A blue callout tag with the entry price (e.g. "0.37869") points at the "+" from above and to the right. This replaces the current plain blue price tag.
   - "Get ready to Long": a blue ↑ arrow under the candle with grey text "Get ready to Long" below it, no box; mirrored for Short (red ↓ above the candle). A small blue ▶ marker on the candle where the alert fired.
   - Redrawn on the last bar only, so it never piles up on history. Shown when "Show Helper" is on.
   - **During an open trade (replaces the old P1 #1 trailing-line idea, agreed 15 Oct 2026):** always show the opposite "+" (normal size, side colour: red for the next Short, green for the next Long) at the price where the next signal would flip the trade, even when it is far away. Comparing it with the red stop line shows which exit comes first.
   - **Bubble:** plain blue tag (option B, Predictum style), white monospace text, placed just right of the "+" at the same price with a small left pointer and a gap. No connector line. Wording:
     - Normal mode, "+" inside the stop: "Next Short at 2,756.72 / this Long closes +7.3% there"
     - Normal mode, "+" beyond the stop: "Next Short at 2,111.00 / your stop (−8%) hits first"
     - "Use the opposite signal as a Stop-Loss" on (no fixed stop): always "Next Short at X / this Long closes ±x% there" (can be a loss)
     - Mirrored for a Short ("Next Long at …").
   - **Price-scale marker:** a small box in the side colour on the right price scale at the next-signal price, like TradingView's own price labels.
   - **Setting:** new toggle under HELPER SETTINGS, "Show next-signal tag on the current trade" (default on). Off hides the blue bubble only; the "+" and the price-scale marker stay.
   - Mock: `research/mocks/approved/p0-2_next_signal_plus_and_blue_tag.png` (all approved mocks: `research/mocks/README.md`).
3. **Predictum X–style trade background, light and dark (moved up from P1 on 15 Oct 2026; VANA and GPS light screenshots, API3 dark screenshot `research/x/x_dark_api3.png`).**
   - The trade's shading starts at the stop line and runs to the chart edge on the profit side, instead of covering the full chart height. Long: from SL up to the top (teal). Short: from SL down to the bottom (pink). Nothing is shaded on the far side of the stop.
   - It runs from the entry candle to the exit candle, with the red SL line along its edge.
   - New input under "Highlight the background": style "SL to edge (Predictum X)" (default) or "Full height (Predictum)".
   - Works in both themes, following the existing "Light theme" switch. Light: teal #5e9fa3 / pink #f48fb1 at ~55 % transparency (X look). Dark (match the API3 X screenshot): deep teal box (≈ #26a69a at ~85 % transparency) for longs and deep maroon (≈ #f23645 at ~80 % transparency) for shorts, so candles and TP lines stay readable.
   - Mocks: `research/mocks/approved/p0-3_x_background_light.png`, `research/mocks/approved/p0-3_x_background_dark.png`.
   - Build note: draw it as a box from the SL to a far price. Check in TradingView that the far edge doesn't squash the price scale. If it does, cap the box at the highest high (Long) or lowest low (Short) of the visible trade plus a margin.
4. **12 coin presets using the original Predictum strategies** (moved up from P1 on 15 Oct 2026; top-coin scan done 15 Oct 2026, 40 coins, results in `research/orig_strategies_top_coins.csv`). Add a Strategy menu entry per qualifying coin; Auto picks it on that coin. A coin qualifies only if the strategy made money in both 2024–25 and 2026 (Binance futures, 45m, 1×, fees 0.08 %). One strategy per coin (the best one). Strategies: ETH = 450 / 0 % / 8 %, BTC v.5 = 210 / 0 % / 6 %, BTC v2.2 = 180 / 0.6 % / 6 %.
   - **Add (✓):**
     - ZECUSDT.P (BTC v.5): +1244 % (2024–25 +207 %, 2026 +338 %), DD 60 %, PF 3.5. Mostly the big 2025–26 ZEC trend.
     - DOGEUSDT.P (ETH): +328 % (+249 %, +23 %), DD 45 %
     - QNTUSDT.P (ETH): +143 % (+10 %, +120 %), DD 61 %
     - ETHUSDT.P (ETH, already in): +141 % (+49 %, +62 %), DD 29 %
     - 1000PEPEUSDT.P (BTC v.5): +110 % (+79 %, +18 %), DD 48 %
     - XRPUSDT.P (ETH): +101 % (+77 %, +13 %), DD 62 %
     - AAVEUSDT.P (ETH): +100 % (+90 %, +6 %), DD 48 %
     - SOLUSDT.P (BTC v.5): +49 % (+25 %, +20 %), DD 45 %
     - PAXGUSDT.P (BTC v2.2): +36 % (+4 %, +31 %), DD 11 %. Gold: small gains, very low drawdown. Data from Mar 2025.
   - **Add with ⚠ (one weak period or deep drawdown):**
     - SUIUSDT.P (ETH): +171 % (+168 %, 2026 only +1 %), DD 45 %
     - UNIUSDT.P (BTC v2.2): +117 % (+12 %, +94 %), DD 66 %
     - ARBUSDT.P (BTC v2.2): +180 % (2024–25 only +1 %, +177 %), DD 49 %
   - **Not added:** AKE (ETH +1385 %, but listed Sep 2025 with only 4 trades before 2026 and DD 76 %; candidate for the P2 "Experimental" group), PUMP (+18 %, DD 52 %, short history).
   - **Did not qualify (lost money in one or both periods on all three strategies):** BTC, BNB, ADA, LINK, AVAX, HYPE, TAO, EGLD, ARC, BCH, BTW, ENA, FIL, INJ, LTC, NEAR, ONDO, OP, PYTH, Q, STRK, TRUMP, WAL, WLD, ZEREBRO, ZK.
   - **Naming (Predictum convention, same as P0 #1):** "<SYMBOL>.P - Binance Futures | 45 min timeframe". The strategy used stays internal and is shown in the tooltip, not the name. The menu order follows the list below. Existing BTC entries keep their suffix: "BTCUSDT.P - Binance Futures | 45 min timeframe" (v2.2) and "… | 45 min timeframe | v.5".
     - ZECUSDT.P - Binance Futures | 45 min timeframe
     - DOGEUSDT.P - Binance Futures | 45 min timeframe
     - QNTUSDT.P - Binance Futures | 45 min timeframe
     - ETHUSDT.P - Binance Futures | 45 min timeframe
     - 1000PEPEUSDT.P - Binance Futures | 45 min timeframe
     - XRPUSDT.P - Binance Futures | 45 min timeframe
     - AAVEUSDT.P - Binance Futures | 45 min timeframe
     - SOLUSDT.P - Binance Futures | 45 min timeframe
     - PAXGUSDT.P - Binance Futures | 45 min timeframe
     - SUIUSDT.P - Binance Futures | 45 min timeframe
     - UNIUSDT.P - Binance Futures | 45 min timeframe
     - ARBUSDT.P - Binance Futures | 45 min timeframe
   - The ⚠ (SUI, UNI, ARB) is kept out of the name so the legend stays clean. It appears in the input tooltip and as a small note in the stats table.

## Dropped
- **Next-signal trailing line / "◀ EXIT" stub (old P1 #1, 15 Oct 2026):** replaced by the opposite "+" and its blue bubble in P0 #2.
- **Move the stop to entry after +3 %** (15 Oct 2026): Predictum's take-profits are tight (0.3 / 1 / 2 / 3 %), so +3 % is already TP4. A breakeven stop there would cut trades inside the TP ladder.
