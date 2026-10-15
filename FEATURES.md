# OG Breakout — features

Original Predictum recreation (clean-room). Current build: **OG X v.2.4.2** (`indicator/og_x.pine`). History: `indicator/VERSIONS.md`. Research: `RESEARCH.md`.

## Engine (Predictum's, recovered and verified)
- **Channel breakout on 45m bars.** Long level = highest high of the last N 45m bars (excluding the current one) × (1 − buffer). Short level = lowest low × (1 + buffer).
- **Entry:** fills intrabar the moment price touches the level, at max(open, level) for longs or min(open, level) for shorts. No candle close is needed.
- **One position at a time.** A touch of the opposite level flips the position.
- **Same-side re-entry** after a stop, on the next touch of that side's level.
- **Verified:** reproduces Predictum's 50-signal BTC history (times and peak-profit labels) and its BTC statistics block (8026.84 % total, 160.54 % average, 47/50, 100 % last 15).
- **No repaint:** only closed 45m bars build the channel (request.security with [1] and lookahead_on).

## Strategies (Strategy dropdown)
| Strategy | N (45m bars) | Buffer | Stop | Notes |
|---|---|---|---|---|
| Auto | — | — | — | BTC chart → v2.2; ETH chart → ETH; other coins → Custom |
| BTCUSDT.P \| 45 min \| v2.2 | 180 | 0.6 % | 6 % | Predictum v2.2.x (Dec 2021 – Jan 2022 entries matched to the cent) |
| BTCUSDT.P \| 45 min \| v.5 | 210 | 0 % | 6 % | Predictum v.5 (50/50 signals matched) |
| ETHUSDT.P \| 45 min | 450 | 0 % | 8 % | Predictum ETH statistics (21/30 exact, rest within a day) |
| Custom | input | input | input | Custom take-profit list too |
Take-profits (Predictum strategies): 0.3 / 1 / 2 / 3 / 10 %. Short TPs = entry / (1 + p).

## Stop-loss behaviour
- **Default ("whichever is closer"):** a trade ends at the fixed stop or at the next opposite signal, whichever is hit first. The opposite signal always flips the position, so it acts as a trailing stop that only moves in the trade's favour.
- **"Use the opposite signal as a Stop-Loss" (switch):** no fixed stop; the trade is held until the next opposite signal. More room, and no cap on a single loss.
- **Measured, ETH 450 settings, Oct 2024 – Oct 2026, 1×, fees:** the default beat or matched "next signal only" on 6 of 9 coins. "Next signal only" won on ETH (+175 % vs +141 %), but its worst single trades were −13.6 % (ETH) up to −43 % (BNB), against −8.1 % with the default.

## Settings (Predictum layout)
- **Strategy**
- **GENERAL SETTINGS:** Highlight the background · Show take-profit labels · Additional labels for position entry ("LONG was opened at …") · Show position opening time · Large size of entry / peak-profit labels · Show averaging levels (7 / 15 / 25 %, display only) · Use the opposite signal as a Stop-Loss
- **HELPER SETTINGS:** Show Helper ("Get ready to Long / Short" within 0.5 % of the next entry, plus a blue price tag on the next entry) · Show SL/TP of the next position · Show SL/TP of the current position · Text size: small · Light theme
- **STATISTICS** (as in Predictum PRO): Show the statistics block · Statistics background · Number of recent signals (50) · Position
- **CUSTOM STRATEGY:** channel length, buffer, stop, take-profit list
- **EXTRA (not in Predictum):** leverage for % labels (10×) · realised results row (exit at stop or next signal, 1×) · fees (0.08 %)

## Chart and statistics
- Background green/red by the last signal. "Long"/"Short" labels. Optional entry box with price and time. TP/SL lines per trade. Peak-profit label that follows the best price (×10). Stopped trades whose peak never reached TP1 show −SL × 10.
- Header tag ("OG Breakout v2.1 ETHUSDT.P - BINANCE Futures | 45 min timeframe"). WARNING box when the chart is above 45m.
- **Statistics block (Predictum style):** newest-first list with emojis (🚫 🤔 😚 😎 🙌 🔥 🎰), 💵 TOTAL (max. profit), 1️⃣ AVERAGE, 👍 WINNING signals (2 TP+), 💎 ACCURACY for the last N and the last 15. Optional realised row.
- **Alerts:** entry with the full TP/SL plan, each TP reached, stop-loss hit, get ready, plus Long / Short alertconditions.

## Ideas and build list
**The live list with priorities (P0 bugs / P1 agreed / P2 ideas) is `BUILD_QUEUE.md`.** Nothing is built until the user says "build"; then the whole queue ships as one version. The list below is the history of ideas.

Status: **Queued** = agreed, waiting to be built. **Idea** = discussed, not decided. **Dropped** = decided against.
1. **Queued — show the next-signal line on the current trade.** Under "Show SL/TP of the current position", also draw the next opposite signal as a dashed trailing line, so it's visible which of the fixed stop and the next signal is closer (as in `research/stop_mock.png`). Label whichever is active "effective stop".
2. **Queued — strategy type "SL" / "DCA + SL"** (Predictum PRO). Enter with ¼, add ¼ at −7 / −15 / −25 %, TPs from the average price, final stop 8 % beyond the last level, held until the opposite signal or the stop. Show averaging buys used per trade and the worst-case loss (~22 % of capital). Tooltip: low leverage only. Backtest Oct 2024 – Oct 2026: ETH 450 +42 % (DD 11 %) vs fixed stop +141 % (DD 29 %); BTC 210 +2 % (DD 12 %) vs −23 % (DD 42 %).
3. **Dropped (15 Oct 2026) — move the stop to entry after +3 %.** Not pursued: with Predictum's tight take-profits (0.3 / 1 / 2 / 3 %), +3 % is already TP4, so a breakeven stop would mostly sit inside the TP ladder and cut trades short.
4. **Idea — one alert for all coins** (hub, Telegram-ready), like `og_shot_hub.pine`.
5. **Idea — re-check on the full history** (`tools/fetch_max_data.py`, 24 coins from 2019) before trading real money.
6. **Idea — "Experimental" group** for settings that only look good on recent months (e.g. EGLD 15m 500 / 0.4 % / 8 %), clearly marked as not validated.
7. **Reference — tuned presets from v1.3–v1.5** (Universal 500 / 0.6 % / 3 %, Fast … Very slow, coin-tuned, timeframe scaling) stay in `indicator/archive/`. Research in `RESEARCH.md` if they are wanted again.
