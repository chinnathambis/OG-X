# OG X (Predictum / OG Breakout) — notes for working sessions

Original Pine v6 channel-breakout indicator (45m), clean-room study of Predictum (public screenshots, videos and price data only; none of its code; not affiliated). Start with `README.md` (repo map), `BUILD_QUEUE.md`, `indicator/VERSIONS.md`, `RESEARCH.md`. Approved mocks: `research/mocks/` (`MOCKS.md`). Current build: `indicator/og_x.pine`.

## How the owner wants to work
- Owner: Chinnathambi (IST, works from an iPhone). Plain-English explanations; no jargon without a line of meaning.
- **Build list first:** answer questions and add fixes/features to `BUILD_QUEUE.md` with a priority (P0, P1, …). Change code only when the owner says **build**, then build the whole list in one go.
- **Mock before building** visual changes; keep approved mocks and note why others were dropped. Dropped ideas stay in the docs, struck through with the reason.
- **Versions:** bump the version on every build; the previous file goes to `archive/` with its version in the name; log it.
- **Studies and back-tests never change the indicator by themselves:** report results, the owner decides.
- Pine can't be compiled here: the owner pastes the file into TradingView and reports errors. Say what still needs checking there.
- Read only the files a task needs. Nothing is kept on the owner's Mac: this repo is the only copy, so commit every build. Never commit keys or secrets.
- Docs moved here from the claude.ai Project on 23 Oct 2026; the repo is the master copy.
