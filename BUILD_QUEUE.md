# OG Breakout — build queue

Items agreed or discussed but not built yet. Newest decisions on top. When an item ships, move it to `indicator/VERSIONS.md`.

## Queued
1. **Strategy type: "SL" / "DCA + SL"** (added 15 Oct 2026, user asked)
   - Like Predictum PRO's "DCA + SL". Entry with ¼ of the position. Add ¼ more at −7 / −15 / −25 % from the first entry. Take-profits are counted from the average price. The final stop sits 8 % beyond the last averaging level. The trade is held until the opposite signal or the stop.
   - The stats table should show the results on full capital (TOTAL, accuracy, the realised row), the number of averaging buys used per trade, and the worst-case loss if all levels fill (≈ 22 % of capital for the default levels).
   - Inputs: strategy type, DCA distances, size per step, stop beyond the last level.
   - Backtest, Oct 2024 – Oct 2026 (full capital, fees): ETH 450 +42 % (DD 11 %) vs fixed stop +141 % (DD 29 %); BTC 210 +2 % (DD 12 %) vs −23 % (DD 42 %). On ETH no trade reached the third level.
   - Warn in the tooltip: low leverage only (1–2×). At 10× a full DCA loss wipes out the account.

## Discussed, not decided
- **Move the stop to entry after +3 %** (optional switch). Helped the slower presets in the exit study; on the ETH chart it would have turned the 13 Mar 2026 −8 % trade into ~0 %.
- **One alert for all coins** (hub, Telegram-ready messages), like `og_shot_hub.pine`.
- **Re-check on full history** (`tools/fetch_max_data.py`, 24 coins, from 2019) before trading real money.
- **"Experimental" preset group** for settings that only look good on recent months (e.g. EGLD 15m 500 / 0.4 % / 8 %, which lost before Jul 2026), clearly marked as not validated.
