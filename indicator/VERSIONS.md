# OG Breakout — versions

The current build is always `indicator/og_breakout.pine`. Every released version is kept in `indicator/archive/`.

| Version | Date | File | Changes |
|---|---|---|---|
| v1.0 | 15 Oct 2026 | `archive/og_breakout_v1.0.pine` | First build. Donchian engine on 45m, intrabar touch entry, presets BTC 180/0.6%, BTC 210/0%, ETH 450/0%, Custom. TP ladders, peak-profit labels, get-ready labels, stats table, alerts. Compiled in TradingView without errors. |
| v1.1 | 15 Oct 2026 | `archive/og_breakout_v1.1.pine` | Fees input (default 0.08% round trip), deducted from the realised stats. Never released on its own: the change shipped inside v1.2. |
| v1.2 | 15 Oct 2026 | `archive/og_breakout_v1.2.pine` | Default preset "Universal · 500 · 0.6% · 3%" (tuned on 12 coins, 2024–2026). "✓ validated / ⚠ not validated on this coin" note in the stats header. |

| v1.3 | 15 Oct 2026 | `archive/og_breakout_v1.3.pine` | 17 presets: 9 Universal-family (Fast 60 → Very slow 850), 5 coin-tuned (BTC, ETH, SOL, DOGE, SUI), 3 original Predictum. Old preset names renamed ("Predictum BTC · 180 · 0.6% · 6%" …), so TradingView resets the preset once. The header check is now per preset: "✓ profitable here in train + test" or "⚠ not validated on this coin". max_bars_back 1000. |

| v1.4 | 15 Oct 2026 | `archive/og_breakout_v1.4.pine` | Tuning bug fixed (short trades closed on a flip were scored as entry/exit − 1 instead of 1 − exit/entry, overstating winning shorts). Presets re-checked: "✓" coin lists updated, "SOL tuned" removed (its 2026 test turned negative). 16 presets. Engine and chart unchanged. |

| v1.5 | 15 Oct 2026 | `archive/og_breakout_v1.5.pine` | Engine timeframe defaults to the chart's. Preset channel lengths are converted to time and scaled to the engine timeframe (Universal = 500 × 45m ≈ 15.6 days = 125 × 3h …), so presets work on 15m, 45m, 1h, 2h or 4h charts. The stats header shows bars ≈ days. max_bars_back 5000, channel capped at 4,900 bars with a warning. On a 45m chart the signals are identical to v1.4. |

| **v2.0** | 15 Oct 2026 | `archive/og_breakout_v2.0.pine` | **Back to the original Predictum.** Rebuilt from v1.0. Only the three recovered Predictum strategies (BTC 180, BTC 210, ETH 450) plus Custom, with "Auto (by chart coin)" as default (BTC chart → BTC 180, ETH chart → ETH 450). Engine fixed on 45m. Predictum-style statistics: newest-first list with emojis, TOTAL (max. profit), AVERAGE, WINNING signals (2 TP+), ACCURACY last N / last 15, default 50 signals. Checked against Predictum's BTC table: 8026.84% total, 160.54% average, 47/50, 100% last 15. The realised row is optional (off). v1.1–v1.5 (extra presets, timeframe scaling) stay in the archive only. |

| v2.1 | 15 Oct 2026 | `archive/og_breakout_v2.1.pine` | Settings laid out like Predictūm v2.2.3 / v2.4.2: Strategy · GENERAL SETTINGS (Highlight the background, Show take-profit labels, Additional labels for position entry, Show position opening time, Large size of entry/peak labels, Show averaging levels, Use the opposite signal as a Stop-Loss) · HELPER SETTINGS (Show Helper, Show SL/TP of the next position, Show SL/TP of the current position, Text size: small, Light theme) · STATISTICS from Predictūm PRO (show block, background colour, number of recent signals). Engine fixed on 45m (no timeframe input). Header tag "OG Breakout v2.1 BTCUSDT.P - BINANCE Futures \| 45 min timeframe" and a Predictum-style WARNING box on a chart above 45m. Custom strategy and extras (leverage, realised row, fees) in their own groups at the bottom. |

**When releasing a new version:** bump the header line, copy the file to `archive/og_breakout_vX.Y.pine`, and add a row here.
