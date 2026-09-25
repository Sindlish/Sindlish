# Sindlish — Development Roadmap

**Version:** 0.1.1 · **Status:** Core language usable · **Tests:** 523 passing

> **Live tracking lives on GitHub.** All forward work is broken into issues and
> grouped under [milestones](https://github.com/Sindlish/Sindlish/milestones).
> Every language-change issue is a self-contained **SEP** (Sindlish
> Enhancement Proposal) written to the [SEP-template](SEP-template.md)
> standard. This file is the *narrative* — the "why" and the ordering. For the
> "what" and "who is working on it", see the milestones.

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

- Pre-1.0, breaking changes are fair game — the language is still being designed.
- Versioning is **sequential**: `v0.1.1` → `v0.2.0` → `v0.3.0` → … → `v1.0.0`.
- Every release is a **deep, meaningful release** — thematically coherent, not a
  point bump.
- The **stability promise lands at v1.0.0**: no breaking changes after that.

---

## Forward plan (GitHub milestones)

| Milestone | Theme | Scope | Home |
|---|---|---|---|
| **v0.2.0 — Expressive Core** | the syntax feels right | `jori` tuples, `bhet`/`haal` pattern matching, block expressions, chaining comparisons, ternary, f-strings, comprehensions, lambdas, do-while, `==`/`aa`, compound assignment, slicing, unpacking, 38 string methods, `chunta`/`tabdeel`/`jama` + utility builtins, `likh(vich=, akhir=)`, `silsilo(shuru=, akhir=, qadam=)` | [milestone/2](https://github.com/Sindlish/Sindlish/milestone/2) · [spec](spec-v0.2.0.md) |
| **v0.3.0 — Data & Serialization** | it reads the real world | file objects + `sang`, bytes type, date/time builtins; JSON, regex, CSV modules | [milestone/3](https://github.com/Sindlish/Sindlish/milestone/3) |
| **v0.4.0 — Object System** | it models real things | `jamaat` classes, `__bunyaad__`, `haso`, `nasal` inheritance, `walid`, `gun` properties, Sindhi dunders, `abstrak` | [milestone/4](https://github.com/Sindlish/Sindlish/milestone/4) |
| **v0.5.0 — Modules & Standard Library** | it scales to real projects | `shamil` import system, package search paths, first stdlib modules | [milestone/7](https://github.com/Sindlish/Sindlish/milestone/7) |
| **v0.6.0 — Type System** | it's safe at scale | optional/nullable, union types, aliases, generics, type checking & inference | [milestone/8](https://github.com/Sindlish/Sindlish/milestone/8) |
| **v0.7.0 — Concurrency** | it does many things at once | threads/goroutines, channels, async/await, sync primitives | [milestone/9](https://github.com/Sindlish/Sindlish/milestone/9) |
| **v0.8.0 — FFI & System** | it talks to everything | C FFI, process mgmt, environment, networking | [milestone/10](https://github.com/Sindlish/Sindlish/milestone/10) |
| **v0.9.0 — Developer Experience** | it's a joy to use | debugger, profiler, formatter, linter, test framework, docs, package manager | [milestone/11](https://github.com/Sindlish/Sindlish/milestone/11) |
| **v0.10.0 — Performance** | it's fast | bytecode optimizations, JIT experiment, memory improvements | [milestone/12](https://github.com/Sindlish/Sindlish/milestone/12) |
| **v1.0.0 — The Standalone Language** | it's real | all features stable, backward-compat guarantee, complete docs, deployment story | [milestone/5](https://github.com/Sindlish/Sindlish/milestone/5) |
| **post-1.0 — The Bumpy Ride** | beyond | Rust/JIT rewrite experiment (in `tools/`), concurrency deepening, FFI, networking | [milestone/6](https://github.com/Sindlish/Sindlish/milestone/6) |

Design decisions that need a human call before code carry the `decision` label;
exploratory prototypes carry `experiment` and are **not** committed to any milestone.

---

## Settled design decisions (grilling session, 2026-09-14)

### Philosophy

- **Naming:** Sindhi for the core language; external standards keep their names
  (`json`, `http`, `regex`).
- **Syntax:** current middle ground — no more ceremony, no less.
- **Breaking changes:** allowed at any pre-1.0 release.

### v0.2.0 — Expressive Core

> **Full design: [`roadmap/spec-v0.2.0.md`](spec-v0.2.0.md)** — the definitive reference.
> This table is the short version.

| Feature | Settled syntax |
|---|---|
| Ternary | `x agar cond warna y` (Sindhi only — `?` is reserved for Result unwrap) |
| F-strings | `"...{expr}..."` (no prefix); `{{` escapes a literal `{` |
| Comprehensions | `[expr har x mein list]`, filtering with trailing `agar`, transform with `agar … warna …`; list/dict/set kinds; multiple iterables zip-style |
| Lambda | `kaam(args) wapas expr` |
| Do-while | `kar { ... } jistain cond` |
| Equality | `==` deep structural, `aa` identity |
| Tuple | `jori` — `(1, 2, 3)`, immutable, `(1,)`, deep-equal, `gharn()`/`jaga()` |
| Pattern matching | `bhet x { haal 1 { ... } haal _ { ... } }` — literals, `_`, bindings, tuple destructuring |
| Block expressions | `{ ... }` auto-yield last expr; `:`→dict, commas→set, else block; vars leak; `wapas` illegal inside |
| Chaining comparisons | `a < b <= c`, mixed operators, method calls |
| Compound assignment | `+= -= *= /= %= ^=` (power is `^`, so no `**`) |
| Slicing | `list[a:b:c]`, negative indices, copy not view, on fehrist/lafz/jori |
| Unpacking | `a, b = [...]`, `a, *rest = [...]`, swap, strings unpack, eval-RHS-then-store |
| String methods | 38, all Sindhi-named; `warha()`→fehrist, `gadh()` accepts fehrist or jori |
| Functional builtins | `chunta(cond_fn, list)`, `tabdeel(fn, list)`, `jama(fn, list)` — function-first |
| Utility builtins | `zbaar` (enumerate), `jora` (zip), `badlo` (cast), `ashl` (truthiness), `lambai` (len alias) |
| `likh` kwargs | `likh("a", "b", vich=", ", akhir="!\n")` |
| `silsilo` kwargs | `silsilo(shuru=1, akhir=10, qadam=2)`, `silsilo(qadam=2, akhir=10)` |
| Break / continue | `tor` = break, `jari` = continue (unchanged; `bhet` is the match keyword) |

### v0.3.0 — Data & Serialization

- **Moderate core:** file I/O + date/time built-in; JSON, regex, CSV are modules.
- **File objects:** `khol(path, mode)` → object with `parho` / `likho` / `band`.
- **Context manager:** `sang file = khol("x") { ... }` — any object with a
  `band()` method.
- **Bytes type:** `b"..."` literals, included in v0.3.0.

### v0.4.0 — Object System

| Concept | Settled syntax |
|---|---|
| Constructor | `__bunyaad__` |
| Inheritance | `jamaat Dog nasal Animal { ... }` |
| Super | `walid.method()` |
| Properties | `gun { mil { ... } rak(val) { ... } }` |
| Abstract | `abstrak jamaat Shape { ... }` |

Dunder methods (16, Sindhi names in `__dunder__` form): `__bunyaad__` (init),
`__lafz__` (str), `__numaish__` (repr), `__barabar__` (eq), `__cut__` (sub),
`__zarab__` (mul), `__vand__` (div), `__poorvand__` (floordiv), `__pachi__`
(mod), `__taqat__` (pow), `__manfi__` (neg), `__musbat__` (pos),
`__faislo__` (bool), `__silsilo__` (iter), `__aglo__` (next), `__lambai__` (len).

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

*Last updated: September 2026 — milestones restructured to the v0.2.0 → v0.10.0 plan*