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

## Saving usage (owner, 1 Nov 2026: "take control on usage")
Claude manages this; the owner doesn't have to.
- **One topic per chat.** When a topic is done or a chat gets long (many hours, big files read, or after one squeeze-down), say so in one line and suggest a fresh chat with a ready one-line starter (e.g. "Mock P1-33 from BUILD_QUEUE"). Keep `CLAUDE.md` and the build list current so a fresh chat needs nothing else.
- **Read narrowly:** grep or read the few lines needed; never whole large files (`.pine`, `index.html`, `trader.py`) unless the task needs them; don't re-read what is already in the chat.
- **Mocks:** one round, at most 2 options, phone size, real code + sample data; small changes are described in words, not re-rendered. Re-render only after the owner's full review list.
- **Answers:** short by default; detail when asked or when money or trading is at stake.
- **Builds:** whole list in one go; one test run in CI rather than repeated local runs; one commit per build.
- **Heavy work off the chat:** back-tests and studies run on GitHub Actions; only results come back.
- **No helper agents or web searches** unless the task really needs them.
