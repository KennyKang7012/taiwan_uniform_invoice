# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                                                      # install dependencies
uv run python scraper.py                                     # fetch latest invoice data → data.json
uv run python generator.py                                   # render data.json + index.css → index.html
uv run python scraper.py && uv run python generator.py       # full pipeline
open index.html                                              # verify output in browser (macOS)
```

No test suite exists. Manual verification: run the pipeline, confirm `data.json` contains expected periods and prize keys, then check `index.html` visually at desktop and mobile widths.

## Architecture

Two-stage pipeline: **scrape → generate → static HTML**.

1. **`scraper.py`** — Fetches winning numbers from Taiwan's Ministry of Finance (財政部) e-tax website. Dynamically computes the current ROC year (AD − 1911), fetches the last 2 years of bimonthly periods (6 total), parses prize numbers from HTML tables via BeautifulSoup4, and writes structured output to `data.json`. Includes defensive fallbacks for DOM changes and 0.5s rate limiting between requests.

2. **`data.json`** — Intermediate data store. Array of period objects, newest-first, each with `period` (民國年 label), `numbers` (dict of prize category → list of numbers), and `url`.

3. **`generator.py`** — Reads `data.json` and `index.css`, renders `index.html` via an embedded Jinja2 template. Embeds CSS inline for single-file static deployment. Defines prize metadata (8 categories, amounts, match rules).

4. **`index.css`** — Source styles. Do not edit `index.html` directly for styling; update this file instead.

5. **`index.html`** — Generated output. Do not hand-edit except for debugging; regenerate via `generator.py`.

6. **`.github/workflows/update_invoices.yml`** — Runs the full pipeline on a cron schedule on odd-numbered months (days 25–27, 08:00 UTC) and auto-commits the result as the github-actions bot.

## Conventions

- Labels in output must remain Traditional Chinese (e.g., `特別獎`, `增開六獎`).
- Parsing logic in `scraper.py` must stay defensive — the Ministry of Finance site DOM has changed before.
- Commit style: `fix(scraper):`, `docs:`, `feat:`. The `auto: update invoice numbers [YYYY-MM-DD HH:MM]` prefix is reserved for the GitHub Actions workflow.
- If adding tests, place them under `tests/test_*.py`.
