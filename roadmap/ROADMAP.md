# Sindlish — Development Roadmap

**Version:** 0.1.1 · **Status:** Core language usable · **Tests:** 523 passing

> **Live tracking lives on GitHub.** All forward work is broken into issues and
> grouped under [milestones](https://github.com/Sindlish/Sindlish/milestones).
> This file is the *narrative* — the "why" and the ordering. For the "what" and
> "who is working on it", see the milestones.

---

## Where Sindlish stands (v0.1.1)

| Area | Status |
|---|---|
| Lexer / Parser / AST | Done — comments, strings incl. triple-quote, full precedence chain, `{ }` blocks |
| Types & variables | Done — `adad`, `dahai`, `lafz`, `faislo`, `khali`; 6 declaration styles; `pakko` consts; typed collections |
| Operators | Done — arithmetic, comparison, logical (`aen`/`ya`/`nah`) |
| Control flow | Done — `agar`/`yawari`/`warna`, `jistain`, `har … mein`, `tor`, `jari` |
| Collections | Done — `fehrist`, `lughat`, `majmuo` with ~35 native methods |
| Functions | Mostly done — `kaam`, typed/default params, `*args`/`**kwargs`, recursion, closures, `bahari` |
| Result error system | Done — `ok()`/`ghalti()`, postfix `?` / `!!`, `.bachao()`, `.lazmi()`, panic + call-stack tracebacks |
| Bytecode backend | Done — slot-based locals, static type checks, shared constant pool, inlined dispatch |
| CLI & REPL | Done — `run`/`repl`/`eval`/`tokens`/`ast`/`check`/`docs`/`--version` |
| Tooling & distribution | Done — VS Code extension, Windows/macOS/Linux installers, benchmarks |
| Object model | Foundational — `SdType`/`SdShey` with C3 MRO; **dormant until `jamaat` classes ship** |

---

## Release discipline

- Backward compatible within the **v0.1.x** line; breaking changes only at a deliberate major bump.
- Releases follow Zig's practice:
  1. All work lands on `main` as merged feature branches.
  2. Release notes are written **incrementally** in `roadmap/release-notes/` as features land.
  3. Feature freeze → tag `vX.Y.Z-rc1` → regression sweep → `rc2` … → final tag.
  4. Every release ships with long-form, technically-deep release notes.

---

## Forward plan (GitHub milestones)

| Milestone | Scope | Home |
|---|---|---|
| **v0.1.2 — Phase A + Ergonomics** | `match`, compound assignment, slicing, string methods, ternary `x agar cond warna y`, `likh(sep=, end=)`; then `lambai`, comprehensions, unpacking assignment, deep value-equality, f-strings, extra casts | [milestone/2](https://github.com/Sindlish/Sindlish/milestone/2) |
| **v0.1.3 — Production Trinity** | File I/O, JSON, `jamaat` classes (constructor, `haso`/self, attribute access, inheritance on the C3 MRO), optional types | [milestone/3](https://github.com/Sindlish/Sindlish/milestone/3) |
| **v0.2.0 — Modules & Standard Library** | `shamil` import, package search paths; stdlib: math, string utils, date/time, CSV, regex | [milestone/4](https://github.com/Sindlish/Sindlish/milestone/4) |
| **v1.0 — Standalone Language** | Type aliases, generics, type guards; benchmark-driven VM perf pass; the stability promise | [milestone/5](https://github.com/Sindlish/Sindlish/milestone/5) |
| **post-1.0 — The Bumpy Ride** | Rust/JIT rewrite experiment (in `tools/`), concurrency, async/await, FFI, networking | [milestone/6](https://github.com/Sindlish/Sindlish/milestone/6) |

Design decisions that need a human call before code carry the `decision` label;
exploratory prototypes carry `experiment` and are **not** committed to any milestone.

---

## Labels

- **Priority:** `priority: P0` → `priority: P3`
- **Area:** `area: core-language`, `area: stdlib`, `area: tooling`, `area: docs`, `area: vscode-extension`, `area: packaging-ci`
- **Kind:** `bug`, `enhancement`, `language-feature`, `correctness`, `refactor`, `documentation`, `perf`, `decision`, `epic`, `experiment`
- **Entry point:** `good-first-issue`, `help wanted`

---

## Pointers

- **Contribute:** [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Canonical docs:** the mdBook in [`book/`](../book) (*Sindlish Internals — A Cozy Field Guide*)
- **Discussions:** [GitHub Discussions](https://github.com/Sindlish/Sindlish/discussions)

*Last updated: September 2026 — moved planning to GitHub milestones*