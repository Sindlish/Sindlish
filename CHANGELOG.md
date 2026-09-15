# Changelog

All notable changes to Sindlish are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### SEP standard — self-contained proposals

Every language-change issue is now a **SEP** (Sindlish Enhancement Proposal)
written to `roadmap/SEP-template.md` — a PEP-grade format with a header pragma
(SEP number, Author, Status, Type, Milestone, Priority, Created) and the body
sections Abstract · Motivation · Specification · Backwards compatibility ·
Implementation plan · Testing · Key references.

- SEPs are **self-contained**: the full design lives in the issue body, with no
  references to local files. Key references link only to other issues.
- v0.2.0's 15 design issues rewritten to the SEP standard (issues #46–56,
  #70–73); 5 new SEPs added (#74–78) for a total of 20 self-contained SEPs;
  the consolidation spec lives at `roadmap/spec-v0.2.0.md`.

### Repo infrastructure — GitHub-first work tracking

The project is now tracked entirely through GitHub milestones and issues. The
standalone `roadmap/FEATURE_ROADMAP.md` and `roadmap/TODO.md` documents have been
deleted (history preserved in git); `roadmap/ROADMAP.md` is the single canonical
narrative and points readers to the live milestone board.

#### GitHub project scaffolding

- **Labels**: priority (`P0`–`P3`), area (`core-language`, `stdlib`, `tooling`, `docs`, `vscode-extension`, `packaging-ci`), kind (`language-feature`, `correctness`, `epic`, `experiment`); stale `phase-0..7` labels and the duplicate `good first issue` removed
- **Milestones**: v0.1.2 — Phase A + Ergonomics, v0.1.3 — Production Trinity, v0.2.0 — Modules & Stdlib, v1.0 — Standalone Language, post-1.0 — The Bumpy Ride
- **Discussions** enabled
- **Description, homepage and topics** refreshed

#### Issue templates

| Template | Labels |
|---|---|
| 🐛 Bug report | bug — *refit: TODO.md check replaced with issue search* |
| ✨ Feature request | enhancement, language-feature |
| 🎯 Task | — (milestone-driven) |
| 📖 Documentation | documentation |
| 🔒 Security vulnerability | bug |
| 💬 Question | question |
| 🔧 Refactor task | refactor — *phase-0..7 dropdown removed, generalised* |

#### Code of Conduct

- Added `CODE_OF_CONDUCT.md` — Contributor Covenant v2.1

#### Pull request template

- Replaced phase-oriented checklist with issue/milestone-driven workflow;
  `Fixes #NN` convention, milestone + labels applied to linked issues

#### Stale-URL sweep

- All references to `AmanatAliPanhwer/Sindlish` across repo config, docs,
  book, and extension updated to `Sindlish/Sindlish`; the VS Code Marketplace
  publisher field (`AmanatAliPanhwer`) is intentionally unchanged

#### Documentation

- `CONTRIBUTING.md`: new "How Work Is Tracked" section (issues → milestones →
  labels workflow), clone URL updated, Code of Conduct link added
- `README.md`: CI/CoC/license shields, "Roadmap & Planning" section linking to
  milestones + Discussions, Code of Conduct link under License
- `book/src/*`: all `roadmap/TODO.md` and `FEATURE_ROADMAP.md` references
  replaced with current pointers (CHANGELOG, closed issues, `ROADMAP.md`)
- `book/book.toml` and `book/src/appendix-distribution.md`: URLs point to the
  new org
- `pyproject.toml`, `install.sh`: upstream URLs updated

### Roadmap

- New canonical narrative in `roadmap/ROADMAP.md`:
  - v0.1.1 status snapshot and release discipline (backward compat within v0.1.x)
  - Milestone table with direct links
  - Label legend and contribution pointers

## [0.1.1] - 2026-09-10

129 commits since v0.1.0.

### Install

```bash
uv tool install git+https://github.com/Sindlish/Sindlish.git
# or: pip install git+https://github.com/Sindlish/Sindlish.git
sindlish eval "likh('Salam dunya!')"
```

One-file installers for **Windows, macOS, and Linux** are attached to this release.

### Language & runtime

- New `bahari` closures — nested functions capture outer variables with correct cell/slot handling
- `silsilo` replaces `range`; set intersection renamed `milap` → `mushtarak`
- `kharabi` unified into `ghalti`; `match` is reserved (clean syntax coming later)
- Lazy ranges, Result-boundary unwrapping, and a bug sweep across lexer → parser → resolver → compiler → VM
- Stricter typing: custom-type validation, missing-annotation errors, `[]` element types on parameters

### Errors — unified philosophy (8-class taxonomy)

- All arithmetic returns a `Result` (parcel) instead of crashing; ordering comparisons raise; equality is total
- `kwarg` clashes, top-level `wapas`, `bahari` misuse, and unknown outer names now get precise, classified errors
- Recursion depth is capped and safety holes from the audit are closed

### Performance

- Inlined VM dispatch loop; O(1) constant deduplication; faster numeric fast-paths and operand unwrapping
- Precomputed `CallPlan` metadata, fast single-pass binding for simple calls, lazily-built Result flags
- New benchmark tool with multiple drivers and JSON/table reporting

### Tooling & packaging

- Installable package with a real `sindlish` CLI: `run`, `repl`, `eval`, `tokens`, `ast`, `check`, `docs`
- `Interpreter` facade exposes `lex → parse → resolve → compile → build_vm → check`; `sindlish check` validates syntax *and* semantics without running
- Offline documentation bundled — `sindlish docs` works offline
- Single-source versioning, hatchling build, PyInstaller spec, one-shot extension updater tool

### VS Code extension (0.1.1)

- First public release. Syntax highlighting, snippets, and linting for `.sd`; grammar is generated from the language's own keyword/builtin registries so it never drifts; semantic diagnostics via the new `check` mode

### Docs

- The mdBook *Sindlish Internals — A Cozy Field Guide* is now the single canonical docs source, with appendices for the AST, grammar, distribution, and extension; the old `docs/` submodule and `developer-docs/` were removed
- Entire API, CLI, and error model documented in code

### Quality & licensing

- **522 tests passing**, ruff clean, golden-bytecode + operand-encoding test harnesses
- Released under **GPL-3.0-or-later** (`LICENSE`)

## [0.1.0] - 2026-04-28

First public release of Sindlish.