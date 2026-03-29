# Repository Guidelines

## Project Structure & Module Organization
- Root scripts:
  - `scraper.py`: fetches winning numbers from the Ministry of Finance site and writes `data.json`.
  - `generator.py`: reads `data.json` and `index.css`, then renders `index.html` via Jinja2.
- Frontend artifacts:
  - `index.html`: generated static page (do not hand-edit unless needed for debugging).
  - `index.css`: UI styles embedded into generated HTML.
- Documentation:
  - `README.md` for usage.
  - `docs/` for SRS, implementation notes, and troubleshooting records.
- Automation:
  - `.github/workflows/update_invoices.yml` for scheduled updates and auto-commit.

## Build, Test, and Development Commands
- `uv sync`: install project dependencies from `pyproject.toml`/`uv.lock`.
- `uv run python scraper.py`: crawl latest periods and update `data.json`.
- `uv run python generator.py`: regenerate `index.html` from current data.
- `uv run python scraper.py && uv run python generator.py`: full local refresh flow.
- Optional quick check: open `index.html` in a browser and verify period switching + prize rendering.

## Coding Style & Naming Conventions
- Language: Python 3.11+.
- Follow PEP 8 basics: 4-space indentation, `snake_case` for functions/variables, `UPPER_CASE` for constants.
- Keep parsing logic defensive (site DOM can change). Prefer small helper functions and clear fallbacks.
- Keep user-facing labels in Traditional Chinese consistent with existing terms (e.g., `特別獎`, `增開六獎`).
- Avoid broad refactors in generated files; update source scripts/styles instead.

## Testing Guidelines
- No formal test suite exists yet (`pytest` not configured).
- Validate changes by:
  1. Running scraper + generator locally.
  2. Confirming `data.json` contains expected periods and prize keys.
  3. Manually checking `index.html` layout and interactions on desktop/mobile widths.
- If adding tests, place them under `tests/` and name files `test_*.py`.

## Commit & Pull Request Guidelines
- Follow current commit style from history:
  - `fix(scraper): ...`
  - `docs: ...`
  - `auto: update invoice numbers [YYYY-MM-DD HH:MM]` (reserved for workflow).
- PRs should include:
  - Scope summary and rationale.
  - Before/after notes for scraper behavior or UI.
  - Updated docs/screenshots when UI changes (`docs/screenshots/`).
  - Linked issue (if applicable) and manual verification steps performed.
