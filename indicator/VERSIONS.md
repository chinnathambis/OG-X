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

**When releasing a new version:** bump the header line, copy the file to `archive/og_breakout_vX.Y.pine`, and add a row here.
