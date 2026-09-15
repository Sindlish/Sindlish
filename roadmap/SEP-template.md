# SEP Template — Sindlish Enhancement Proposal

Every Sindlish language change is a **SEP** — a self-contained proposal written to
PEP-grade standard. One SEP = one GitHub issue.

**A SEP must be self-contained.** Everything a reviewer or implementer needs —
the current behavior, the proposal, the exact syntax/semantics, edge cases,
implementation plan, and test strategy — lives *inside the issue body*. SEPs do
**not** reference local files, roadmap documents, or other issues except as
numbered links under **Key references**.

---

## Header pragma

```
SEP:        <number — use the GitHub issue number>
Title:      <concise feature title>
Author:     <name or GitHub handle>
Status:     Draft | Accepted | Implemented | Rejected | Withdrawn
Type:       Language Feature | Standard Library | Tooling | Info | Process
Milestone:  <vX.Y.Z — milestone name>
Priority:   P0 | P1 | P2 | P3
Created:    <YYYY-MM-DD>
```

Status lifecycle:
- **Draft** — design not yet settled.
- **Accepted** — settled by grilling; ready to implement.
- **Implemented** — merged into the milestone.
- **Rejected / Withdrawn** — closed without implementation (add a one-line reason).

---

## Body sections

### Abstract

Two or three sentences: what this SEP adds, why in one breath.

### Motivation

Why the language needs this today. Only state the *problem*; the *how* belongs
to Specification. Keep it honest — if a feature's only rationale is "Python has
it", say so and give the Sindhi-specific reason it matters.

### Specification

The full, unambiguous contract. Include:

- **Syntax** — a grammar sketch or settled form, with a minimum of two concrete
  examples in valid Sindlish.
- **Semantics** — every behavior in plain language. Spell out edge cases:
  evaluation order, mutability, aliasing, error behavior, scoping.
- **Grammar / parser notes** — new tokens, precedence position, disambiguation
  rules (e.g. how `{ }` is told apart from dict/set/block).

If the item interacts with another feature, specify that interaction here
(e.g. how unpacking behaves when the RHS is a `jori`).

### Backwards compatibility

What changes relative to v0.1.x, and whether the break is acceptable. Pre-1.0
breaking changes are allowed but must be *named* — never accidental.

### Implementation plan

Step list across the pipeline, one bullet per stage touched:

```
[ ] lexer        — new tokens / literal scanners
[ ] parser       — AST nodes, precedence, disambiguation
[ ] resolver     — scoping, slot/label effects
[ ] compiler     — new opcodes / operand shapes
[ ] vm           — runtime semantics, new Sd* types
[ ] objects      — new SdType / SdShey immutability story
[ ] builtins     — runtime/builtins.py entries
```

### Testing

The specific test plan, mapped to the repo's existing suites (golden-bytecode
harness, operand-encoding harness, semantics suite, error suite):

- golden-bytecode snapshots for the new AST/opcodes
- positive semantics cases (one per behavior)
- negative cases (compile errors, runtime Ghalti classes)
- error-class mapping — which Sindhi error fires for each failure mode

### Key references

Numbered links to *other issues or Discussions only* (e.g. the `aa` keyword,
tuple patterns, reduce ordering). No local file paths.