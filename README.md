# Predictum research → OG Breakout

A clean-room study of the Predictum crypto indicator. The conclusions come from its public screenshots, videos and Binance price data; none of its code was used. The result is **OG Breakout**, an original Pine Script v6 indicator.

## Repository
| Path | What |
|---|---|
| `indicator/og_breakout.pine` | OG Breakout v1.0 (Pine v6). Paste into TradingView's Pine Editor. |
| `RESEARCH.md` | The findings: engine rules, fitted presets, TP/SL ladders, reality-check backtest. |
| `tools/fetch_data.py` | Downloads Binance USDT-M futures 15m candles into `data/` (run on a machine that can reach Binance). |
| `tools/fetch_presets_data.py`, `tools/tune_presets.py`, `tools/grid_all.py` | 2-year data for 12 coins and the preset tuner |
| `research/*.csv` | Tuning grid results |
| `tools/fit_engine.py` | Loader, 45m resampler, simulator and the 80 ground-truth signals. Prints `BTC v.5 matched 50 / 50`. |
| `research/screenshots/`, `research/videos/` | Source material collected from public posts. |

## Quick start
```
python3 tools/fetch_data.py      # creates data/BTCUSDT_15m.csv, data/ETHUSDT_15m.csv
python3 tools/fit_engine.py      # -> BTC v.5 matched 50 / 50
```

## The engine in one paragraph
A Donchian channel breakout on 45-minute bars. Long when price touches highest(high, N)[1] × (1 − buffer). Short when it touches lowest(low, N)[1] × (1 + buffer). Entry fills intrabar, one position at a time, a fixed % stop, a fixed % take-profit ladder, and a same-side re-entry after a stop. The original Predictum BTC presets are N = 180 with a 0.6% buffer, or N = 210 with none; both use a 6% stop. The tuned default for 2024–2026 is **Universal: N 500, 0.6% buffer, 3% stop**, validated on 10 coins (see RESEARCH.md).

Not affiliated with Predictum. For research and education; not financial advice.
