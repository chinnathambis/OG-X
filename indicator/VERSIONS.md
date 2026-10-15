# OG Breakout — versions

The current build is always `indicator/og_breakout.pine`. Every released version is kept in `indicator/archive/`.

| Version | Date | File | Changes |
|---|---|---|---|
| v1.0 | 15 Oct 2026 | `archive/og_breakout_v1.0.pine` | First build. Donchian engine on 45m, intrabar touch entry, presets BTC 180/0.6%, BTC 210/0%, ETH 450/0%, Custom. TP ladders, peak-profit labels, get-ready labels, stats table, alerts. Compiled in TradingView without errors. |
| v1.1 | 15 Oct 2026 | `archive/og_breakout_v1.1.pine` | Fees input (default 0.08% round trip), deducted from the realised stats. Never released on its own: the change shipped inside v1.2. |
| v1.2 | 15 Oct 2026 | `archive/og_breakout_v1.2.pine` | Default preset "Universal · 500 · 0.6% · 3%" (tuned on 12 coins, 2024–2026). "✓ validated / ⚠ not validated on this coin" note in the stats header. |

| v1.3 | 15 Oct 2026 | `archive/og_breakout_v1.3.pine` | 17 presets: 9 Universal-family (Fast 60 → Very slow 850), 5 coin-tuned (BTC, ETH, SOL, DOGE, SUI), 3 original Predictum. Old preset names renamed ("Predictum BTC · 180 · 0.6% · 6%" …), so TradingView resets the preset once. The header check is now per preset: "✓ profitable here in train + test" or "⚠ not validated on this coin". max_bars_back 1000. |

**When releasing a new version:** bump the header line, copy the file to `archive/og_breakout_vX.Y.pine`, and add a row here.
