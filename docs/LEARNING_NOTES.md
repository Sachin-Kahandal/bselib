# bselib Modernization — A Learning Walkthrough

This document explains **every change** made when modernizing `bselib`, written for someone
learning what "professional Python project standards" actually mean and *why* they exist.

Each section follows the same shape:

- **The idea** — the concept in plain language
- **Why it matters** — the problem it solves
- **Before → After** — what changed in this repo
- **Try it yourself** — commands you can run to see it

There were **12 commits**. Run `git log --oneline master..HEAD` to see them. The commit
*prefixes* (`feat:`, `fix:`, `build:`…) are themselves a standard — explained in §1.

---

## Mental model: what is "a Python package"?

A package is just code organized so other people (and tools) can **install and run it
reliably**. "Modernizing" means making four groups happy:

1. **Humans** reading the code (formatting, types, docs).
2. **The installer** (`pip`/`uv`) — it needs to know the name, version, and dependencies.
3. **Automation** (CI) — robots that re-check your work on every change.
4. **Future-you** — who won't remember why anything was done (hence tests + decision logs).

Everything below serves one of those four.

---

## 1. Git hygiene — branches & commit messages

### The idea
Git records history. Good history is **readable**: each commit is one logical change with a
message explaining *why*.

### Why it matters
When something breaks in 6 months, `git log` and `git blame` are your time machine. Messy
history ("fixed stuff", "update", "asdf") makes that machine useless.

### Before → After
- **Branch:** all work went on a new short-lived branch `chore/modernize-package` instead of
  committing straight to `master`. The prefix tells you the *kind* of work.
  - Convention: `feat/`, `fix/`, `chore/`, `docs/` + a short `kebab-case` description.
- **Conventional Commits:** every commit message starts with a *type*:
  - `feat:` new feature · `fix:` bug fix · `docs:` documentation · `refactor:` restructure
    without behavior change · `test:` tests · `build:`/`ci:`/`chore:` tooling & plumbing.
  - Format: a ~50-char imperative subject ("add X", not "added X"), then a blank line, then a
    body explaining **why**. Tools can auto-generate a CHANGELOG from these.
- **Atomic commits:** one logical change per commit. We deliberately *split* the packaging
  change apart from the layout move so each commit does exactly one thing.

### Try it yourself
```bash
git log --oneline master..HEAD     # the 12 commits
git show 14e887b                    # read one commit in full
```

---

## 2. Packaging — `setup.py` → `pyproject.toml`

### The idea
Every package needs a **manifest**: its name, version, dependencies, supported Python
versions. Historically this lived in executable `setup.py`. The modern standard is a
**declarative** file, [`pyproject.toml`](../pyproject.toml) (defined by "PEP 621").

### Why it matters
- `setup.py` is *code that runs* — error-prone and slow. The old one even had a typo
  (`ducumentation=`) that was silently ignored, so the docs URL never made it into the package.
- Declarative TOML is just data: tools read it without executing anything.
- It's the **single source of truth** — packaging, linter, type-checker, and test config all
  live in one file under `[tool.*]` sections.

### Before → After
| Before (`setup.py`) | After (`pyproject.toml`) |
|---|---|
| `version="0.0.5"` hard-coded in two places | version declared once; code reads it via `importlib.metadata` |
| classifiers claimed Python 2.7–3.7 (all dead) | `requires-python = ">=3.9"` |
| `ducumentation=` typo (ignored) | proper `[project.urls]` |
| no build backend declared | `[build-system]` uses `hatchling` |

**"PEP"** = Python Enhancement Proposal, the numbered design docs that define these standards.
PEP 621 = how to write `[project]` metadata.

### Try it yourself
```bash
cat pyproject.toml          # read the whole manifest
python -c "import bselib; print(bselib.__version__)"
```

---

## 3. `src/` layout

### The idea
Put the package inside a `src/` folder: `bselib/` → [`src/bselib/`](../src/bselib).

### Why it matters
Without `src/`, when you run tests from the project root, Python imports the **local folder**
`bselib/` directly — even if the package was never actually *installed* correctly. That hides
packaging bugs. With `src/`, your code is only importable if it was genuinely installed, so
your tests exercise the package the way a real user would. It's a "test what you ship" guard.

### Try it yourself
```bash
ls src/bselib/              # the package now lives here
```

---

## 4. Dependencies, lockfile & `uv`

### The idea
- **Dependencies** = other libraries your code needs (here: `requests`, `beautifulsoup4`,
  `pandas`, `lxml`, `html5lib`).
- **`uv`** = a fast, modern tool that creates the virtual environment, installs deps, and
  manages the lockfile — one tool replacing `pip` + `venv` + more.
- **Lockfile** ([`uv.lock`](../uv.lock)) = an exact record of *every* package version
  installed, including sub-dependencies.

### Why it matters
- **Pinning:** the old manifest said `bs4>=0.0.1` — "any version from a broken ancient one
  upward." That can install something that doesn't work, or a future version that breaks you.
  We tightened to floors *and* ceilings, e.g. `beautifulsoup4>=4.9,<5` (allow 4.x, block the
  unknown 5.0).
- **Lockfile = reproducibility:** "works on my machine" happens when two people get different
  sub-dependency versions. The lockfile guarantees everyone — and CI — installs the *exact*
  same set. This is why it's committed to git.
- **Dev vs runtime split:** users of `bselib` need `requests`; they do **not** need `pytest`
  or `ruff`. Those are in a separate `[dependency-groups] dev` list, so `pip install bselib`
  stays lean.

### Try it yourself
```bash
uv sync                     # create .venv and install everything from the lockfile
uv run python -c "from bselib import BSE; print(BSE())"
```
(`uv run` runs a command inside the managed environment automatically.)

---

## 5. Code formatting & linting — `ruff`

### The idea
- **Formatter** = auto-arranges code (spacing, quotes, line breaks) so style is consistent and
  never debated.
- **Linter** = scans for likely mistakes and bad patterns (unused imports, risky constructs).
- **`ruff`** does both, extremely fast, configured in `pyproject.toml` under `[tool.ruff]`.

### Why it matters
Consistent style means diffs show *real* changes, not whitespace noise. The linter catches
bugs before they run. Example it caught here: **bare `except:`**.

### Before → After
```python
# Before — catches EVERYTHING, even Ctrl-C and system-exit signals
try:
    ...
except:
    return error

# After — catches real errors but lets you Ctrl-C out of a hung request
try:
    ...
except Exception:
    return error
```
`ruff` also rewrote `dict()` → `{}`, sorted imports, and flagged `== None` → `is None`.

### Try it yourself
```bash
uv run ruff format .        # auto-format
uv run ruff check .         # lint (reports problems; --fix to auto-fix)
```

---

## 6. Type hints & `mypy`

### The idea
**Type hints** annotate what kinds of values a function takes and returns:
```python
def quote(script_code: int | str) -> dict[str, Any]:
```
**`mypy`** is a *static type checker* — it reads those hints and proves your code is consistent
**without running it**.

### Why it matters
- They're **documentation that can't go stale** — the checker enforces them.
- They catch whole classes of bugs (passing the wrong type, forgetting a return).
- The marker file [`py.typed`](../src/bselib/py.typed) tells *other people's* type checkers
  "this package has types, use them" — so your users get autocomplete and checking too.

A real example from this repo: `mypy` flagged that `soup.select_one("h1")` can return `None`,
so calling `.get_text()` on it could crash. We added a guard. That's a bug found by *reading*,
never having to hit the website.

### Try it yourself
```bash
uv run mypy                 # "Success: no issues found"
```

---

## 7. Testing — the big one

### The idea
**Tests** are code that checks your code. `pytest` is the standard runner: any function named
`test_*` that doesn't crash = pass.

This library is 100% web scraping, which creates a problem: **tests must not depend on a
website being up** (that would make them slow and flaky). The solution is three layered ideas:

#### a) Fixtures + mocking
A **fixture** is saved sample data. We captured **real** responses from BSE/Screener/etc. once
and saved them under [`tests/fixtures/`](../tests/fixtures). **Mocking** means swapping the real
`requests.get` for a fake that returns those saved files. So tests replay reality — fast,
offline, and **deterministic** (same input → same result, every time).

See [`tests/conftest.py`](../tests/conftest.py): an *autouse fixture* automatically installs
the fake for every test.

#### b) The contract test (the clever part)
A scraper rots silently: a website changes its HTML and your parser quietly returns nothing.
The **contract test** in [`tests/test_contract.py`](../tests/test_contract.py) declares the
exact HTML selectors / JSON keys each parser depends on, then:
- *offline:* checks the saved fixture still contains them (so fixtures can't drift from code).
- *live (opt-in):* fetches the **real** site and checks they're still there — so if BSE
  changes its markup, a test fails loudly and tells you to fix the scraper.

> This immediately earned its keep: it caught that Screener had renamed its pros/cons HTML
> containers, so `analysis()` had been silently returning empty results. See commit `3cf306c`.

#### c) Markers & coverage
- A **marker** tags tests: `@pytest.mark.live` flags the network tests. Our config deselects
  them by default (`-m 'not live'`) so normal runs and CI stay offline; you opt in with
  `-m live`.
- **Coverage** measures what % of your code the tests actually execute (we're at 81%). The goal
  is *meaningful* coverage, not a magic number — note we test the error paths too.

### Why it matters
Tests are what let you change code *confidently*. Without them, every edit is a gamble.

### Try it yourself
```bash
uv run pytest               # offline tests
uv run pytest --cov         # with a coverage report
uv run pytest -m live       # hit the real sites (needs internet)
```

---

## 8. Continuous Integration (CI) — GitHub Actions

### The idea
**CI** = a robot that runs your checks automatically on a clean machine every time you push.
Ours is defined in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

### Why it matters
"It passes on my laptop" isn't proof — your laptop has random stuff installed. CI runs on a
fresh machine, so green CI means it genuinely works. Our pipeline is the classic four stages:

**install → lint → type-check → test**

It also uses a **matrix**: it runs the tests on Python 3.9, 3.10, 3.11, 3.12, and 3.13 in
parallel, proving the library works on every version you claim to support.

### Try it yourself
The robot runs on GitHub after you push. Locally, the same commands are:
```bash
uv run ruff check . && uv run mypy && uv run pytest
```

---

## 9. Pre-commit hooks

### The idea
A **git hook** runs automatically at a git event. [`.pre-commit-config.yaml`](../.pre-commit-config.yaml)
runs ruff + mypy **before each commit**.

### Why it matters
It catches issues *before* they're even committed, so CI rarely fails on something trivial.
CI is the safety net; pre-commit is catching it at your desk first. (Opt-in:
`uvx pre-commit install`.)

---

## 10. Dependency update automation — Dependabot

### The idea
[`.github/dependabot.yml`](../.github/dependabot.yml) is a GitHub robot that watches your
dependencies and opens pull requests to bump them when new versions ship.

### Why it matters
Dependencies get security fixes and bug fixes. Manually tracking them is tedious and easy to
forget; Dependabot does it on a weekly schedule.

---

## 11. Documentation & project meta

### The idea
Docs are part of the product. We added/updated:
- **README badges** — the little status images at the top of [`README.md`](../README.md). They
  show, at a glance: is CI passing? what's the latest version? which Pythons are supported?
- **Quickstart** — copy-pasteable examples so a new user is productive in 30 seconds.
- **[`CHANGELOG.md`](../CHANGELOG.md)** — a human-readable list of what changed per release,
  following the "Keep a Changelog" format and **Semantic Versioning** (`MAJOR.MINOR.PATCH`:
  bump MAJOR for breaking changes, MINOR for features, PATCH for fixes).
- **[`SECURITY.md`](../SECURITY.md)** — how to report a vulnerability privately.
- **[`DESIGN_DECISIONS.md`](../DESIGN_DECISIONS.md)** — "ADR-lite". An **ADR** (Architecture
  Decision Record) captures *why* a choice was made, so future-you doesn't undo it by accident.
  Every change in this project added an ADR entry.

### Why it matters
Code says *what* it does; docs say *why* and *how to use it*. The "why" is the part that's
expensive to reconstruct later.

---

## 12. What we deliberately did NOT do (and why that's correct)

Good engineering is also knowing what to *skip*:
- **Publishing to PyPI / git tags / GitHub Releases** — these are "outward-facing" actions; we
  set up all the machinery but didn't actually publish, by choice.
- **Request timeouts/retries** — a runtime behavior change, out of scope for this pass.
- **CONTRIBUTING guide, issue/PR templates, code-review gates** — these matter for *teams*; for
  a solo educational project they're overhead. Skipping them on purpose is the right signal.

---

## Glossary (quick reference)

| Term | Plain meaning |
|---|---|
| **PEP** | A numbered Python standard document |
| **`pyproject.toml`** | The one config file describing the package + its tools |
| **build backend** | The tool that turns your code into an installable file (hatchling) |
| **wheel / sdist** | The built package files (`.whl` = ready-to-install, `.tar.gz` = source) |
| **lockfile** | Exact pinned versions of everything, for reproducible installs |
| **virtual environment** | An isolated Python + libraries, separate from your system |
| **linter** | Finds likely mistakes/bad patterns |
| **formatter** | Auto-arranges code style |
| **type hint** | Annotation of what type a value is |
| **static analysis** | Checking code without running it (mypy, ruff) |
| **fixture** | Saved test data / reusable test setup |
| **mock** | A fake stand-in for something real (here, the network) |
| **CI** | Automation that re-runs your checks on every push |
| **matrix** | Running the same job across many versions/configs |
| **coverage** | % of code your tests execute |
| **ADR** | A written record of a design decision and its reasoning |
| **SemVer** | `MAJOR.MINOR.PATCH` version numbering scheme |

---

## The 5-minute daily workflow

Once set up, your everyday loop is just:
```bash
uv sync                        # (first time / after dep changes)
# ... edit code ...
uv run ruff format .           # tidy
uv run ruff check . --fix      # lint
uv run mypy                    # type-check
uv run pytest                  # test
git commit -m "fix: ..."       # commit (pre-commit re-runs the checks)
```
If all four pass and CI is green, you can trust the change.
