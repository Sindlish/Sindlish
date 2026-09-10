# Changelog

All notable changes to Sindlish are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.1] - 2026-09-10

129 commits since v0.1.0.

### Install

```bash
uv tool install git+https://github.com/AmanatAliPanhwer/Sindlish.git
# or: pip install git+https://github.com/AmanatAliPanhwer/Sindlish.git
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