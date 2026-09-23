# Sindlish v0.2.0 — Expressive Core · Design Spec

**Status:** settled (grilling sessions 2026-09-14 + 2026-09-15)
**Home:** [milestone/2](https://github.com/Sindlish/Sindlish/milestone/2)
**Theme:** *the syntax feels right* — ergonomic sugar that keeps the VM simple and the language complete.

---

## Feature index

| # | Feature | Keyword / syntax | SEP | Priority |
|---|---|---|---|---|
| 1 | Tuple type | `jori` · `(1, 2, 3)` | #73 | P0 |
| 2 | Pattern matching | `bhet` / `haal` | #70 | P0 |
| 3 | Block expressions | `{ ... }` | #71 | P0 |
| 4 | Chaining comparisons | `a < b <= c` | #72 | P1 |
| 5 | Ternary | `x agar cond warna y` | #46 | P0 |
| 6 | F-strings | `"...{expr}..."` | #47 | P1 |
| 7 | Comprehensions | `[expr har x mein list]` | #48, #74 | P1 |
| 8 | Lambdas | `kaam(x) wapas expr` | #49 | P1 |
| 9 | Do-while | `kar { ... } jistain cond` | #50 | P2 |
| 10 | Deep equality / identity | `==` / `aa` | #51 | P1 |
| 11 | Compound assignment | `+= -= *= /= %= ^=` | #52 | P0 |
| 12 | Slicing | `list[a:b:c]` | #53 | P1 |
| 13 | Iterable unpacking | `a, *rest = [...]` | #54 | P1 |
| 14 | String methods | 38 methods | #55, #75, #76 | P2 |
| 15 | Functional builtins | `chunta` `tabdeel` `jama` | #56 | P1 |
| 16 | Utility builtins | `zbaar` `jora` `badlo` `ashl` `lambai` | #77 | P1 |
| 17 | `likh` kwargs | `likh(vich=, akhir=)` | #78, #80 | P1 |

---

## 1. Tuple type — `jori`

Sindhi name: **`jori`** (*pair*) — imported from `fehrist`-family collections.

- Literal: `(1, 2, 3)`. Single-element tuple requires a trailing comma: `(1,)`.
- **Immutable** — no mutation methods, no `+=` append.
- Deep structural `==` (`(1, 2, 3) == (1, 2, 3)` → `sach`); `aa` is identity.
- Indexing `t[0]` returns the element; slicing `t[0:2]` returns a **new `jori`** (never a view).
- Methods: `gharn()` (count) and `jaga()` (index) — same names as the `lafz` methods.
- **Fully separate from `fehrist`.** No implicit coercion. Conversion is explicit:
  - `fehrist(t)` → list copy
  - `jori(f)` → tuple from a list
- Can be destructured (see §13), matched (see §2), and iterated by `har … mein`.

## 2. Pattern matching — `bhet` / `haal`

Syntax:

```
bhet x {
    haal 1 { likh("One") }
    haal "two" { likh("Two") }
    haal (i, j) { likh("pair {i}, {j}") }      # tuple destructuring
    haal koorh { likh("boolean") }
    haal y { likh("bound {y}") }               # bare name binds
    haal _ { likh("something else") }
}
```

- `match` is **`bhet`**; each case is **`haal`**.
- `break` is **`tor`**; `continue` is **`jari`** (unchanged, both legal across block boundaries).
- Pattern grammar:
  - Literals: numbers, strings, `sach`/`koorh`/`khali`.
  - `_` wildcard — matches anything.
  - Bare names bind (Python `case` style — the parser knows number/string/bool/null tokens, so any other name is a binding).
  - Tuples and tuple destructuring `(p1, p2)` where each part is itself a pattern.
- **Exhaustiveness is optional** — a `bhet` without `_` or full coverage is not an error; unmatched values fall through to the end.
- Guards (`haal x agar cond`) are **deferred to v0.3.0**. No fall-through between arms.
- The match subject is evaluated once.

## 3. Block expressions — `{ ... }`

A `{ }` block is an **expression that evaluates to a value**.

- Auto-yield: the block's **last expression** is the block's value.
- Statements may precede it: `{ likh("hi"); 42 }`.
- **`wapas` inside a block is a compile error** (`TarteebJeGhalti`) — it belongs to `kaam` bodies only.
- `tor` / `jari` are legal inside blocks and act on the enclosing loop/match (`bhet` arm). (Python `break`/`continue` behavior; a block is *not* a scope barrier for control flow.)
- Variables declared inside a block **leak to the enclosing scope** (Rust/Go blocks are scopes; these are expression containers — the resolver treats them as the current scope).
- Dead-code rule: a non-final expression statement in a block warns at `check` time (not a hard error).
- **Braces disambiguation** — three meanings, resolved by contents:
  - Contains `:` key-value pairs → **`lughat`** literal.
  - Contains comma-separated exprs with no colon → **`majmuo`** literal.
  - Otherwise → **block expression** (statements / single expression / control flow).
  - `{}` (empty) → empty `lughat`; empty set uses the `majmuo()` constructor.
- Blocks are values everywhere: assignment `adad x = { ... }`, argument `likh({ ... })`, return `wapas { ... }`, ternary arm.

## 4. Chaining comparisons

- `a < b <= c` parses as `a < b` **and** `b <= c` — the middle operand is evaluated **once**.
- Mixed operators allowed: `x >= 5 > y`.
- Method calls allowed anywhere in the chain: `0 < s.lambi() < 10`.
- Existing ordering-comparison raise behavior is preserved.

## 5. Ternary

- `x agar cond warna y` — Sindhi-only; `?` stays reserved for Result unwrap.
- Precedence: sits below `or`/`ya`, above assignment.
- Always returns a value; usable as an rvalue anywhere.
- Integrated into block expressions (a ternary can be the yielding expression).

## 6. F-strings

- `"...{expr}..."` — interpolation inside a **plain string literal**, no prefix.
- `likh("Salam {name}! Umer {age} ahy")`
- Output is a plain `LAFZ`.
- **`{{`** escapes a literal `{`; there is no `\` escape (matches f-string convention).
- Works in triple-quoted strings too.
- Lexer: string scanner handles `{expr}` with nested braces/expressions.

## 7. Comprehensions

All three collection kinds:

```
[x*2 har x mein numbers]                     # list
[x har x mein list agar x > 0]               # filtered (agar last)
[x agar x > 0 warna 0 har x mein list]        # transform-with-default
{x: y*2 har x, y mein items}                  # dict
{expr har x mein list}                        # set
```

- Sources: `fehrist` (values), `lughat` (keys), `majmuo` (elements), and `lafz` and `jori`.
- **Multiple iterables are zip-style** (parallel): `har x mein a, y mein b` zips `a` and `b` like `jora`; stop at shortest.
- Nested comprehensions work.
- Loop variables **do not leak** to the enclosing scope (Python 3 semantics).
- `agar` last without `warna` = filter; `agar … warna` in the element position = transform (Python `if` vs ternary, mirrored).

## 8. Lambdas

- `kaam(x) wapas x * 2` — anonymous single-expression function.
- Parens required: `kaam(x, y) wapas x + y`.
- First-class: passes to `tabdeel`/`chunta`/`jama`, stored in variables, returned from functions.
- Compiles through the same closure machinery as a named `kaam` (closure cells, `bahari`, etc.).
- Complex logic → named `kaam` or a block function; lambdas are single-expression only.

## 9. Do-while

```
kar { ... } jistain cond
```

- Body executes at least once, then condition re-checked.
- `tor` / `jari` behave as in `jistain`.
- Compiler: body, then condition-check + back-jump.

## 10. Equality — `==` vs `aa`

- `==` becomes **deep structural** for collections and tuples: recursive, mixed kinds unequal, total boolean.
  - `[1, [2, 3]] == [1, [2, 3]]` → `sach`
- `aa` = identity: `x aa x` → `sach`; `[1,2] aa [1,2]` → `koorh`.
- `aa` becomes a lexer/resolver keyword (currently unused). Lexer note: `aa` is a prefix of the existing `aalmi` — longest-match keyword scanning required.
- `jori` compares structurally like every other collection.

## 11. Compound assignment

- `x += 1  x -= 1  x *= 2  x /= 2  x %= 3  x ^= 2`
- **`^=`** matches the language's existing power operator `^` (right-assoc). There is **no `**` token**.
- Parser rewrites `x op= y` as `x = x op y` at the AST level (one evaluation of the target).
- Works with subscript targets: `list[0] += 1`, `lughat["a"] -= 1`.
- `pakko` rejects any compound assignment (existing behavior).
- Target must be a valid lvalue (variable or subscript). No collection `+=`.

## 12. Slicing

- `list[a:b]`, `list[a:b:c]`, `list[:2]`, `list[2:]`, `list[::-1]`, `neg[-2:]` — negative indices.
- Applies to `fehrist`, `lafz`, and `jori`. Dicts/sets out of scope.
- Returns a **new** list/string/tuple (copy, never a view).
- Parser disambiguates `x[i]`, `x[a:b]`, `x[a:b:c]` inside `[]`.
- Standalone slice objects out of scope.

## 13. Iterable unpacking

```
a, b = [1, 2]                  # simple
a, b = b, a                    # swap
a, *rest = [1, 2, 3, 4]        # rest = [2, 3, 4]
*head, last = [1, 2, 3]        # head = [1, 2]
a, b = "xy"                    # works on any iterable (str, jori, …)
```

- LHS is comma-separated targets (variables/subscripts) with optional `*` capture (single allowed).
- RHS must be iterable; length mismatch → runtime `JagaJeGhalti` (unless `*` captures the remainder).
- Multiple assignment `a, b = 1, 2` uses the same machinery.
- **Both sides evaluated before any store**; evaluation order is defined (all RHS, then each store left-to-right).

## 14. String methods

Immutability: `lafz` is immutable — every method returns a new string. Methods are on `lafz` only; `jori`/`fehrist` do not inherit them. `warha()` returns a `fehrist`; `gadh()` accepts a `fehrist` **or** `jori`.

| Python | Sindlish | Notes |
|---|---|---|
| `capitalize()` | `wadhakar()` | first letter bigger |
| `casefold()` | `nindhakar()` | normalize to lowercase |
| `center()` | `wich()` | put in the middle |
| `count()` | `gharn()` | count occurrences |
| `encode()` | `ramz()` | encode / coded form |
| `endswith()` | `puchar()` | end with |
| `expandtabs()` | `tabwadh()` | expand tabs |
| `find()` | `ghol()` | search / find |
| `format()` | `saja()` | arrange / format |
| `index()` | `jaga()` | find position |
| `isalnum()` | `adadlafz()` | number or letter |
| `isalpha()` | `lafzi()` | letters only |
| `isascii()` | `asci()` | ASCII only |
| `isdecimal()` | `ashariadad()` | decimal number |
| `isdigit()` | `adad()` | digits |
| `isidentifier()` | `pehchan()` | valid identifier |
| `islower()` | `nindhoaa()` | lowercase |
| `isnumeric()` | `adadnuma()` | numeric |
| `isprintable()` | `chapyo()` | printable |
| `isspace()` | `khaali()` | whitespace |
| `istitle()` | `unwani()` | title case |
| `isupper()` | `waddoaa()` | uppercase |
| `join()` | `gadh()` | join together |
| `ljust()` | `kaabo()` | align left |
| `lower()` | `nindho()` | lowercase |
| `lstrip()` | `kaabolaah()` | remove from left |
| `partition()` | `tukro()` | split into parts |
| `removeprefix()` | `mundhlaah()` | remove prefix |
| `removesuffix()` | `pucharilaah()` | remove suffix |
| `repeat` | `"ha " * 3` | `*` operator repetition (no method) |
| `replace()` | `badla()` | replace |
| `reverse()` | `ulto()` | reverse characters |
| `rfind()` | `ulteghol()` | search from right |
| `rindex()` | `ultejaga()` | index from right |
| `rjust()` | `sajjo()` | align right |
| `rpartition()` | `ultetukro()` | partition from right |
| `rsplit()` | `ultewarha()` | split from right |
| `rstrip()` | `sajjolaah()` | remove from right |
| `split()` | `warha()` | split → fehrist |
| `splitlines()` | `sittwarha()` | split lines |
| `startswith()` | `shrothe()` | start with |
| `strip()` | `laah()` | remove surrounding |
| `swapcase()` | `akroula()` | swap case |
| `title()` | `unwan()` | title |
| `translate()` | `tarjumo()` | map characters |
| `upper()` | `waddo()` | uppercase |
| `zfill()` | `sifarbharr()` | zero-fill |

## 15. Functional builtins

Function-first argument order (settled; consistent across all three):

```
chunta(cond_fn, list)      # filter  → fehrist
tabdeel(fn, list)          # map     → fehrist
jama(fn, list)             # reduce  → single value; no initial-value arg
```

- `jama(fn, list)` folds with `fn(acc, item)`; caller supplies the seed through a closure/`pao` if needed. Works on strings, `jori`, `fehrist`, sets, dicts (keys).
- All three accept a named `kaam` **or** a lambda.

## 16. Utility builtins

```
zbaar(iterable)      # enumerate → fehrist of jori [index, value]
jora(a, b, ...)      # zip → fehrist of jori pairs (shortest wins)
badlo(value, qisam)  # cast: badlo(x, "adad") / badlo(x, "lafz")
ashl(value)          # truthiness: sach→sach, 0→koorh, khali→koorh, []→koorh
lambai(value)        # length (alias for lambi)
```

- `zbaar`/`jora` return **`fehrist` of `jori`** (pairs are fixed-size, immutable).

## 17. `likh` keyword args

```
likh("a", "b", vich=", ", akhir="!\n")
```

- `vich` default `" "`; `akhir` default `"\n"`.
- `chunta`/`tabdeel`/`jama`/`zbaar`/`jora`/`badlo`/`ashl`/`lambai` are **builtins** (global), not methods.

---

## Cross-cutting notes

- **Naming:** Sindhi for core keywords and methods; external formal names (`json`, `regex`) stay English when they arrive (v0.3.0+).
- **Breaking changes allowed** pre-1.0; v0.2.0 deliberately adds `aa`, `bhet`, `haal`, `jori` and redefines `{ }` (block vs dict vs set) — a documented break from v0.1.x string/collection behavior where relevant.
- **`muqabla` (compiler) surface:** new keywords `bhet`, `haal`, `aa`, `jori` (type). `tor`/`jari` semantics unchanged.
- **Composability:** `bhet` + tuple destructuring, blocks inside ternary, comprehensions over `jori` — all stack without special cases.
- **VS Code extension** grammar is generated from the language registries, so keyword additions propagate automatically; the LSP's `check` path picks up the new dead-code warning.
- **Test targets:** golden-bytecode harness needs new snapshots for every new AST node and opcode; extend `tests/` with per-feature suites named `test_v020_*.py`.

---

## Open by design (deferred)

| Feature | Target |
|---|---|
| `bhet` guards (`haal x agar cond`) | v0.3.0 |
| `sang` context manager / file objects / bytes / date-time | v0.3.0 |
| `jamaat` classes, dunders, `walid`, `gun` | v0.4.0 |
| `shamil` modules | v0.5.0 |