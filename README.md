# OG X

**OG X v.2.4.4 + Alerts**: an original Pine Script v6 indicator for TradingView. It trades channel breakouts on 45-minute bars, with presets for 39 coins plus the two BTC strategies, each with a backtest confidence rating. Developed from a clean-room study of the Predictum indicator: public screenshots, videos and exchange price data only, none of its code. Not affiliated with Predictum.

## Repository
| Path | What |
|---|---|
| `indicator/og_x.pine` | **Current build.** Paste into TradingView's Pine Editor. |
| `indicator/archive/` | Every released version (OG Breakout v1.0 – v2.3, OG X v.2.4.0+). |
| `indicator/VERSIONS.md` | What changed in each version. |
| `BUILD_QUEUE.md` | Live build list: P0 / P1 / P2, shipped items and dropped ideas. |
| `FEATURES.md` | Feature list and idea history. |
| `RESEARCH.md` | Findings: engine rules, fits, presets, top-coin scan, Predictum X notes. |
| `research/mocks/` | Approved UI mocks (`README.md` explains each) and superseded ones. |
| `research/screenshots/`, `research/videos/` | Source material from public posts. |
| `research/x/` | Predictum X signal screenshots (`signals/`) and `x_signals.csv`. |
| `research/*.csv` | Tuning grids, timeframe study, top-coin results. |
| `data/*.csv.gz` | Binance USDT-M futures 15m candles (Oct 2024 – Oct 2026, 40 coins, plus BTC/ETH history). `gunzip -k data/*.gz` before running the tools. |
| `data_bybit/*.csv.gz` | Bybit 15m candles around the Predictum X signals. |
| `tools/` | Fetch scripts (run on a machine that can reach the exchange), the fit engine, tuners and studies. |

## Quick start
```
gunzip -k data/*.gz                 # or: python3 tools/fetch_data.py
python3 tools/fit_engine.py         # -> BTC v.5 matched 50 / 50
```

## The engine in one paragraph
A Donchian channel breakout on 45-minute bars. A long fires when price touches highest(high, N)[1] × (1 − buffer); a short fires when it touches lowest(low, N)[1] × (1 + buffer). Entry fills intrabar, with one position at a time. Each trade has a fixed % stop (or the opposite signal), a fixed % take-profit ladder (0.3 / 1 / 2 / 3 / 10 %), and a same-side re-entry after a stop. The strategies are BTC v2.2 (180 bars / 0.6 % buffer / 6 % stop), BTC v.5 (210 / 0 / 6 %) and ETH (450 / 0 / 8 %).

For research and education; not financial advice.
