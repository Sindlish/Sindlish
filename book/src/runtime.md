# Environment, Builtins & the REPL

<div class="youarehere">📍 <strong>You are here:</strong> Part Eight · Living Here — 1 of 3</div>

## 🧠 The globals environment

One dict with discipline: `runtime/env.py` maps names → `VariableRecord(value, type, element_type, is_const)`. That record struct is *why* global const/type enforcement is cheap — checks read the slot next to the value. `define/lookup_record/assign` are the whole API; `assign` refuses on `is_const`.

Builtins are seeded into this environment at startup (`tests/conftest.py` shows the exact recipe): each of the five builtins registered as a const `KAAM`-typed record.

| Builtin | Behavior notes |
|---|---|
| `likh(values..., vich=" ", akhir="\n")` | joins values with `vich`, finishes with `akhir`; does **not** consume Results |
| `puch(prompt)` | returns `SdString` |
| `lambi(x)` | works on strings, lists/dicts/sets, ranges |
| `silsilo([shuru=]akhir[, qadam])` | returns **lazy** `SdRange` (O(1) length, indexable); `shuru`/`akhir`/`qadam` also bindable as keywords |
| `qisam(x)` | returns the type name of `x` as a `lafz` |
| `majmuo([iterable])` | 0 or 1 args |

Keywords reach a builtin only through `kwarg_specs` (`builtins.py`): the VM rejects unknown names, fills declared defaults, and hands the dict over. A builtin whose spec declares `KWARG_UNSET` defaults recovers which names the caller *actually* passed by identity — that is how `silsilo` tells `silsilo(1, 10, qadam=2)` from `silsilo(1, 10, 2)`. Positionals fill `shuru`, `akhir`, `qadam` left to right, so `silsilo(1, 2, akhir=3)` reports the repeated argument rather than quietly shifting slots.

## 🖥️ The REPL (`interpreter/repl.py`)

The REPL reuses the whole pipeline per line with two twists:

1. **Persistence**: every line shares one globals `Environment` (`interpreter/__init__.py:31`), and top-level assignments always compile through the checked `STORE_GLOBAL` path — so names naturally survive across lines, with const/type enforcement intact.
2. **Prompt tooling**: syntax highlighting via a regex pass, plus completion fed by the resolver's `symbols` list — the same data the VS Code extension uses. One producer, two consumers.

Errors in REPL mode don't kill the session: the interpreter reports and keeps the loop alive (file mode exits non-zero instead).

<div class="recap">
<p>Globals = records with enforcement metadata attached.</p>
<p>Builtins seed as const KAAM records; <code>silsilo</code> is lazy.</p>
<p>REPL = pipeline + shared globals environment + symbols-driven completion.</p>
</div>
