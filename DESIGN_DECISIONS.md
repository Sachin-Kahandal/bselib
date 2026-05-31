# bselib — Design Decisions Reference

> **Purpose of this file.** This is the single source of truth for *how* and *why* `bselib`
> is built the way it is. Read it before changing anything. Every design decision made
> **from here on** must be appended to the [Decision Log](#decision-log) at the bottom — each
> entry stating *what* was decided, *why*, and *what it affects*. When in doubt about how to
> implement something, this document — not memory or habit — decides.

- **Project:** bselib — a Python library that scrapes & aggregates BSE / Indian market data
- **Version at time of writing:** 0.0.5
- **License:** MIT
- **Maintainer:** Sachin Kahandal
- **Last reviewed:** 2026-05-31

---

## 1. What this library is (and is not)

`bselib` scrapes and aggregates **real-time and historical financial data** for stocks listed
on the Bombay Stock Exchange (BSE) and related Indian markets. It pulls from BSE's own
endpoints plus several third-party aggregators (MarketsMojo, Screener.in, Yahoo Finance, NSE)
and exposes everything through one simple `BSE()` class.

**It is explicitly an educational / personal-project library, not a production system.**
The docs warn that aggressive scraping can overload target servers and get your IP
blacklisted, and that data is only ever as accurate/available as the upstream websites.

**Guiding principle:** *Breadth and simplicity for learners over robustness and performance.*
Any decision that adds complexity must justify itself against this principle.

---

## 2. Architecture at a glance

```
            User application
                   │
            ┌──────▼──────┐
            │  BSE class  │   bse.py — thin facade, stateless
            └──────┬──────┘
                   │ delegates to module-level functions
   ┌───────┬───────┼────────────┬──────────┐
 quote.py  script.py  statements.py  analysis.py  gainers.py
   │           │          │            │
   └───────────┴──── getId.py ─────────┘   (BSE↔MarketsMojo / Screener ID bridge)
                   │
   ┌───────────────┼──────────────┬───────────────┬────────────┐
 BSE API/site  MarketsMojo    Screener.in    Yahoo Finance   NSE API
```

**Source files** (`bselib/`):

| File            | Responsibility |
|-----------------|----------------|
| `bse.py`        | `BSE` facade class — delegates to the modules below. No logic, no state. |
| `quote.py`      | Live quotes, ratios, bulk deals, holdings, news, corporate actions, company profile. |
| `getId.py`      | Resolves a BSE script code to MarketsMojo IDs / Screener.in URLs. The "bridge" layer. |
| `gainers.py`    | Top gainers/losers of the day + NSE/BSE market status. |
| `script.py`     | Search for a stock by name/code → `{script_code: name}`. |
| `statements.py` | Historical financial statements (via pandas `read_html`) + annual/credit report links. |
| `analysis.py`   | Fundamental analysis, pros/cons, statement analysis (API-first). |

---

## 3. Standing design decisions (the existing contract)

These are the decisions already baked into the codebase. **Honor them by default.** Changing
any of these is a breaking change and must be recorded in the Decision Log with a migration note.

### D1 — Facade pattern via a single `BSE` class
Everything is reached through `BSE()`, which just delegates to module-level functions.
- **Why:** One obvious entry point; learners don't need to know the module layout.
- **Implication:** New features should be exposed as a `BSE` method that delegates to a
  module function. Keep `bse.py` free of business logic.

### D2 — Stateless, no caching, no connection pooling
Every call makes fresh HTTP request(s).
- **Why:** Simplicity; always-fresh data; no cache-invalidation concerns.
- **Implication:** High latency and repeated hits on upstream servers. If caching is ever
  added, it must be opt-in and must not change default behavior. (See open question Q2.)

### D3 — Errors are returned as sentinel dicts, never raised
Standard returns:
- `{'info': 'Error'}` — generic network/parse failure
- `{'info': 'Not a valid script_code'}` — input failed validation
- `{'info': 'please be more specific'}` — search returned nothing
- **Why:** Callers (often beginners) don't have to write try/except.
- **Implication:** Callers must inspect the returned dict. New functions must follow the
  same convention — **do not** introduce raised exceptions into the public API without a
  logged decision. Prefer reusing the existing sentinel constants in `quote.py`.

### D4 — Script codes validated as exactly 6 digits
- **Why:** BSE equity script codes are 6 digits; cheap guard against obvious bad input.
- **Implication:** Keep this validation on any new function that takes a `script_code`.

### D5 — Multi-source aggregation (best data per provider)
Live quotes ← BSE; corporate actions/holdings/news ← MarketsMojo; statements/reports/
pros-cons ← Screener.in; company profile ← Yahoo Finance; market status ← NSE/BSE.
- **Why:** No single source has everything; pick the best/free source per data type.
- **Implication:** Fragile and cross-domain. When adding data, document the source and
  route the ID translation through `getId.py`. Centralize new ID bridges there.

### D6 — Prefer official/JSON APIs over HTML scraping where one exists
`analysis.py` and parts of `quote.py` hit JSON endpoints; `statements.py` and `gainers.py`
still scrape HTML with CSS selectors (incl. fragile `nth-of-type`).
- **Why:** APIs are far less brittle than HTML structure.
- **Implication:** **For new work, prefer a JSON endpoint.** Only scrape HTML when no API
  exists. When you must scrape, isolate the selector and comment what it targets so it's
  easy to fix when the upstream layout changes.

### D7 — Browser User-Agent on every request
All requests send a Chrome `User-Agent` header.
- **Why:** Some upstreams reject the default `python-requests` UA.
- **Implication:** Keep sending it. If a shared `headers` constant exists in the module, reuse it.

### D8 — Values returned as strings (mostly)
Financial figures are largely returned as strings straight from HTML/JSON; `mktCap` etc.
use small nested dicts like `{'in': 'Cr', 'value': ...}`.
- **Why:** Matches scraping output; avoids lossy/locale-dependent number parsing.
- **Implication:** Callers convert to numbers themselves. Keep return shapes stable —
  consumers depend on exact key names.

### D9 — Synchronous, single-attempt I/O (no retries, no timeouts today)
- **Why:** Simplest possible implementation.
- **Implication:** A slow/blocked upstream blocks the caller. Adding timeouts/retries is
  desirable but must be conservative and logged (see Q1).

### D10 — Dependencies: bs4, requests, pandas, html5lib, lxml (loose `>=` pins)
- **Why:** Scraping stack (bs4/lxml/html5lib) + pandas for tabular statement parsing.
- **Implication:** Loose pins (e.g. `bs4>=0.0.1`) are intentionally permissive but risky.
  Tightening them is encouraged but is a logged decision (Q3).

### D11 — No test suite, no type hints today
- **Why:** Historical — the project started as a quick educational tool in 2023.
- **Implication:** This is a known gap, not an intentional preference. New code *should*
  add tests where practical (see Q4). Document any testing approach you adopt below.

---

## 4. Conventions (follow these when writing code)

- **Naming:** functions `snake_case` (`get_gainers`, `historical_stats`); the `BSE` class is
  the only `PascalCase` name. (`getId.py` predates the convention — don't add more camelCase
  module names.)
- **Return shape:** dicts. List results are wrapped under a descriptive key, e.g.
  `{'gainers': [...]}`, `{'bulk_deals': [...]}`. Keep this wrapping for new list endpoints.
- **Dict keys:** processed/derived data uses `snake_case`; raw API passthrough may keep the
  upstream `camelCase`. Don't rename passthrough keys without a logged decision.
- **Error handling:** reuse the D3 sentinel dicts; wrap network/parse code in try/except.
- **New data type checklist:** (1) add module function, (2) bridge IDs via `getId.py`,
  (3) prefer JSON API (D6), (4) validate `script_code` (D4), (5) expose via a `BSE` method
  (D1), (6) document the upstream source here, (7) add a Decision Log entry.

---

## 5. Open questions / candidate decisions (not yet decided)

Resolve these by adding a Decision Log entry when the time comes — don't decide silently in code.

- **Q1 — Request timeouts & retries.** Should every request get a default timeout and a small
  bounded retry? (Improves robustness; risks hammering upstreams — must include backoff.)
- **Q2 — Optional caching.** Worth an opt-in cache for slow/expensive calls? Must default off.
- **Q3 — Tighten dependency pins** (especially `bs4>=0.0.1`) and drop Python 2.7 from classifiers.
- **Q4 — Tests & CI.** Minimum viable test approach given everything depends on live scraping
  (record/replay fixtures? mock HTTP?).
- **Q5 — Type hints.** Introduce gradually on the public `BSE` API?
- **Q6 — Rate limiting** to protect both the user's IP and upstream servers.

---

## 5a. Modernization improvements (prioritized backlog)

Gaps between bselib's current packaging/tooling (legacy `setup.py` + `setup.cfg`, ~2019 era)
and a modern (2024–2026) Python package. Ordered by **importance** — do the higher tiers first;
each higher tier de-risks the ones below it. When you act on an item, log an ADR and tick it here.

### Tier 0 — Does it still work? (verification) — ✅ DONE 2026-05-31

After ~3 years, every public method was run live against Reliance (500325). **Initial state:
10 of 18 working.** Root causes were diagnosed and fixed; **current state: 18 of 18 working.**
See ADR-001/002/003 below. Fixes were all parser/header/source changes — no API redesign.
The deeper lesson (no tests, silent `{'info':'Error'}` hid *why* things broke) is exactly what
Tier 1 addresses; this verification was a manual one-off and should be replaced by ADR-001's tests.

| Was broken | Root cause | Fix |
|---|---|---|
| `quote`, `bulk_deals`, `ratios`, `peers` | `api.bseindia.com` now serves the SPA shell (HTML) unless the request carries `Origin`/`Referer: bseindia.com` | added `bse_api_headers` to those calls (ADR-002) |
| `script` | request omitted the browser `User-Agent` → MarketsMojo returned 403 | pass `headers` (ADR-003) |
| `annual_reports`, `credit_reports` | Screener replaced `div.three:nth-of-type(n)` with `div.annual-reports` / `div.credit-ratings` | new selectors (ADR-003) |
| `comp_profile` | Yahoo decommissioned its `/profile` page (404) | re-sourced from Screener; return shape changed (ADR-001-source-swap → ADR-001 below) |

### Tier 1 — Critical (do first; everything else depends on these)

1. **Test suite with mocked HTTP.** No tests exist today. Because every function hits live
   sites, the library silently rots when an upstream layout/endpoint changes. Use `pytest`
   with record/replay HTTP mocking (`vcrpy` or `responses`) so tests don't depend on BSE being
   up. *Resolves Q4.* **Highest impact: without this, nothing else can be verified.**
2. **CI on GitHub Actions.** No `.github/workflows/` today. Run lint + tests on push/PR across
   a Python version matrix. This is what makes the test suite actually protect you. *Resolves Q4.*
3. **Request timeouts + bounded retries with backoff.** No timeouts today (D9) — a slow/blocked
   upstream hangs the caller indefinitely. Add per-request timeouts and a small retry with
   backoff (`requests` + `urllib3.Retry`, or migrate to `httpx`). *Resolves Q1.*

### Tier 2 — High (foundation & hygiene)

4. **Migrate `setup.py` → `pyproject.toml` (PEP 621).** Declarative metadata + a real
   `[build-system]` backend (hatchling / setuptools / uv). Single-source the version. *Relates to D10.*
5. **Fix broken/stale packaging metadata.** `setup.py` has `ducumentation=` (typo → silently
   ignored, docs URL never reaches metadata) and classifiers claim Python **2.7 / 3.5–3.7**
   (all dead). Set a real `requires-python = ">=3.9"`. *Resolves part of Q3.*
6. **Tighten dependency pins.** `bs4>=0.0.1` permits a broken ancient version; `pandas`/`lxml`
   have no upper bounds, so an upstream major bump can break installs silently. Add sane floors
   and consider upper caps. *Resolves rest of Q3.*
7. **Add a lockfile** (`uv.lock` / `poetry.lock`) for reproducible installs.

### Tier 3 — Medium (code quality & maintainability)

8. **Ruff** for lint + format (replaces flake8/isort/black); centralize config under `[tool.*]`.
9. **Type hints + mypy/pyright** on the public `BSE` API, plus a `py.typed` marker so consumers
   get the types. *Resolves Q5.*
10. **`pre-commit` hooks** to run Ruff/mypy locally before commits.
11. **Structured logging** via the `logging` module instead of silent `except` blocks — keeps
    D3's sentinel-dict returns but makes failures diagnosable (ties to D3/D9).

### Tier 4 — Lower (release process & project hygiene)

12. **Release automation:** git tags (none exist today), `CHANGELOG.md` (Keep a Changelog),
    and PyPI **Trusted Publishing** (OIDC, no stored tokens) on tag.
13. **`src/` layout** to prevent the flat layout from importing the local dir during tests.
14. **Community files:** `CONTRIBUTING.md`, `SECURITY.md`, issue/PR templates.
15. **Dependency-update automation** (Dependabot / Renovate).

### Tier 5 — Optional / nice-to-have

16. **Async / concurrent fetching** (`httpx` async or `aiohttp`) so callers can fetch many
    stocks at once — directly counters the synchronous D9. Only if real demand appears.
17. **Optional caching** for slow/expensive calls, default off. *Resolves Q2.*
18. **Rate limiting** to protect the user's IP and upstream servers. *Resolves Q6.*

> **Note on scope:** Tiers 1–2 are the genuinely important ones for a small educational
> scraping library and are roughly an afternoon's work given the small codebase. Tiers 3–5
> are quality/polish — pursue as the project grows. None of these should violate the guiding
> principle (Section 1): *breadth & simplicity for learners over robustness & performance.*

---

## 6. How to record a new decision

Append to the [Decision Log](#decision-log) using this template. Newest entries at the top.
Keep each entry short and concrete. Once a decision is logged, update the relevant standing
decision (Section 3) or convention (Section 4) if it changes the contract.

```
### ADR-NNN — <short title>
- **Date:** YYYY-MM-DD
- **Status:** Accepted | Superseded by ADR-XXX | Reverted
- **Context:** What prompted this? What constraint or problem?
- **Decision:** What we will do, specifically.
- **Reason:** Why this over the alternatives.
- **Consequences:** What it affects — files, API shape, callers, follow-ups.
```

---

## Decision Log

<!-- Add new decisions here, newest first, using the template in Section 6. -->

### ADR-003 — Repair stale parsers against still-live endpoints
- **Date:** 2026-05-31
- **Status:** Accepted
- **Context:** `script`, `annual_reports`, `credit_reports` returned `{'info':'Error'}` / `{}`
  even though their upstreams were alive. `script` (in `script.py`) omitted the browser
  `User-Agent`, so MarketsMojo answered **403** (note `getId.py` hits the same endpoint *with*
  the header and worked). Screener replaced its old `div.three:nth-of-type(n)` document layout
  with semantic `div.annual-reports` / `div.credit-ratings` containers.
- **Decision:** Pass `headers` on the `script()` request. Replace the report selectors with the
  new container classes via a shared `_report_links()` helper that keeps the
  `{visible text: href}` return shape and skips non-document/button links.
- **Reason:** Smallest change that restores each function without altering its contract.
- **Consequences:** `bselib/script.py`, `bselib/statements.py`. Reinforces D6 (selectors are
  fragile — isolate and comment them) and D7 (always send the UA header).

### ADR-002 — BSE API now requires Origin/Referer headers
- **Date:** 2026-05-31
- **Status:** Accepted
- **Context:** Every `api.bseindia.com/BseIndiaAPI/api/*` call (`quote`'s HighLow, `bulk_deals`,
  `ratios`, `peers`) returned HTTP 200 but with the BSE single-page-app **HTML shell** instead
  of JSON, so `.json()` threw and the catch-all returned `{'info':'Error'}`. BSE began gating
  its API on the request originating from the BSE site. (`ratios` also had a latent bug: its
  second call was made with **no headers at all**.)
- **Decision:** Add a `bse_api_headers` constant (browser UA **+** `Origin`/`Referer:
  https://www.bseindia.com` + JSON `Accept`) and use it for all `api.bseindia.com` calls.
  Also fixed `quote`'s change/pChange sign handling (it string-compared prices and double-signed
  an already-signed value → `--29.45`); now derived numerically.
- **Reason:** The endpoints and response schemas are unchanged — only the access gate is new.
  Adding headers restores 4 methods with zero contract change, far cheaper than a source swap.
- **Consequences:** `bselib/quote.py`. The BSE site could tighten gating further (cookies/tokens);
  if these break again, that *is* the trigger to re-source (revisit D5). Use `bse_api_headers`
  for any new `api.bseindia.com` call.

### ADR-001 — Re-source company profile from Screener (Yahoo profile decommissioned)
- **Date:** 2026-05-31
- **Status:** Accepted
- **Context:** `comp_profile`/`get_profile` scraped Yahoo Finance's `/quote/<sym>/profile`
  page, which Yahoo has removed (now **404**, and Yahoo is heavily JS-obfuscated/auth-gated —
  not reliably scrapeable). The Yahoo search API still works, but the profile page is gone.
- **Decision:** Re-source `get_profile` from Screener.in (already a trusted source in this lib).
  Return `script_code`, `Name`, `description`, `website`, `bse_link`, `nse_link`. **Dropped**
  `symbol`, `sector`, `industry`, and the dynamic CEO/MD key — Screener does not expose them
  cleanly. This is a **breaking change to the return shape** of this one method.
- **Reason:** A partial, reliable profile from an already-used source beats a fully-broken one.
  Avoids adding a new fragile Yahoo-scraping dependency. Consistent with D5 (best source per
  data type) and D6 (prefer sources we can actually parse).
- **Consequences:** `bselib/quote.py`. Any caller reading `sector`/`industry`/`symbol` from
  `comp_profile` must adapt. If those fields are needed later, find a new source and log an ADR.
  This is the first instance of the "BSE/upstream killed an endpoint → swap source" pattern
  flagged in Tier 0; expect more as the other scraped sites evolve.

### ADR-000 — Establish this design reference
- **Date:** 2026-05-31
- **Status:** Accepted
- **Context:** The project was built quickly in 2023 with many implicit design choices spread
  across the code and docs. There was no single place capturing *why* things are the way they
  are, making future decisions inconsistent.
- **Decision:** Maintain this `DESIGN_DECISIONS.md` as the canonical reference. All future
  design decisions are appended to the Decision Log with their reasoning; standing decisions
  (Section 3) describe the current contract.
- **Reason:** A living ADR-style document keeps reasoning discoverable and decisions
  consistent without forcing heavyweight process.
- **Consequences:** Every non-trivial change should check this file first and add an entry
  when it makes or changes a design decision.
