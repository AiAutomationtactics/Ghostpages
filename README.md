# Practical Traffic Lab

Practical, reader-first guides about traffic measurement, opt-in funnels, ethical affiliate marketing, and search content.

## The 20-day plan

- Start: **October 23, 2026**; end after **November 11, 2026** in Vancouver time.
- **Up to five distinct articles per day** (maximum **100 pages** total).
- A first batch of five written guides is included in the `docs/guides` directory.
- Future publishing uses GitHub Actions at **9:17 AM America/Vancouver** (including DST adjustments).
- Pages that fail quality gates are not published; this is a ceiling, not a quota.

## How to activate

1. Enable **GitHub Pages** under **Settings → Pages → Deploy from a branch → main → /docs**. This is required to make the published website publicly accessible.
2. A ChatGPT scheduled task is configured for 19 daily follow-up batches (October 24–November 11), using the connected GitHub account. Its ability to commit should be checked after the first scheduled run; results are not guaranteed.
3. **Optional second publishing route:** add repository secret `OPENAI_API_KEY` under **Settings → Secrets and variables → Actions** to enable GitHub Actions generation. This is a separately billed API key; never commit it into the repository. The GitHub Action uses the same date/page caps and will not publish extra pages once the daily cap is met.
4. Check GitHub **Actions**, the article list and the scheduled task results. A run may be delayed, skipped or blocked by a permission issue.

The website address after GitHub Pages is enabled is https://aiautomationtactics.github.io/Ghostpages/.

See `PUBLISHING.md` for editorial safeguards, link rules, and limitations. Search visibility is not guaranteed.
