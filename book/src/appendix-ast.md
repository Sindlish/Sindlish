# Appendix: AST Node Reference

<div class="youarehere">📍 <strong>You are here:</strong> Appendix · Reference</div>

Every syntactic construct in Sindlish is represented by a `Node` subclass in `interpreter/frontend/ast_nodes.py`. There are **32 node classes**, all subclassing `Node` (which owns `line`/`column` source position). They are `@dataclass(slots=True)` with position initialized at construction and stamped via `set_pos()`.

Fields marked *resolver-stamped* are filled in during the resolver pass, not by the parser.

## Literals

| Node | Fields | Description |
|------|--------|-------------|
| `NumberNode` | `value: int \| float` | Integer or float literal; `get_type()` → ADAD or DAHAI |
| `StringNode` | `value: str` | String literal; `get_type()` → LAFZ |
| `BoolNode` | `value: bool` | `sach` / `koorh` literal |
| `NullNode` | — | `khali` literal |

## Variables & Assignment

| Node | Fields | Description |
|------|--------|-------------|
| `VariableNode` | `name`, `hints*` | Variable reference |
| `AssignNode` | `name, value, type, is_const, element_type, has_explicit_type`, `hints*` | Declaration/assignment (all six declaration styles) |
| `IndexNode` | `left, index, value` | Index access `obj[i]`, or index-assignment `obj[i] = v` when `value` is set |

## Operators

| Node | Fields | Description |
|------|--------|-------------|
| `BinaryOpNode` | `left, op, right` | Binary operation (`+ - * / % ^`, comparisons, `aen`/`ya`) |
| `UnaryOpNode` | `op, right` | Unary operation (`-x`, `nah x`) |
| `PostfixOpNode` | `expr, op` | Postfix `?` / `!!` |

## Statements

| Node | Fields | Description |
|------|--------|-------------|
| `IfNode` | `condition, body, else_body, else_if_bodies` | `agar` / `yawari` / `warna` chain |
| `WhileNode` | `condition, body` | `jistain` loop |
| `ForNode` | `iterator, iterable, body`, `hints*` | `har … mein` loop |
| `BreakNode` | — | `tor` |
| `ContinueNode` | — | `jari` |
| `BlockNode` | `statements` | `{ … }` block |
| `ProgramNode` | `statements, slot_count` | Top level; `slot_count` set by resolver |
| `GlobalNode` | `name` | `aalmi` declaration |
| `NonLocalNode` | `name` | `bahari` declaration |

## Collections

| Node | Fields | Description |
|------|--------|-------------|
| `ListNode` | `elements` | `[a, b]` literal |
| `DictNode` | `pairs` | `{k: v}` literal |
| `SetNode` | `elements` | `{a, b}` literal (dict/set disambiguated by the parser) |

## Functions & Calls

| Node | Fields | Description |
|------|--------|-------------|
| `ParamNode` | `name, type, default, is_star, is_kw, element_type, slot_index` | Function parameter (supports `*args`, `**kwargs`, typed, defaulted) |
| `FunctionNode` | `name, params, body, return_type`, `hints*` | `kaam` definition |
| `CallNode` | `name, args, keywords, star_args, kw_args`, `hints*` | Function call (supports call-site `f(*l)`, `f(**d)`) |
| `MethodCallNode` | `instance, method_name, args, keywords, star_args, kw_args` | `obj.method(...)` |
| `GetAttrNode` | `instance, attr_name` | `obj.attr` |
| `ReturnNode` | `value` | `wapas` |

## Result System

| Node | Fields | Description |
|------|--------|-------------|
| `ResultConstructorNode` | `variant, value` | `ok(value)` / `ghalti(value)` |
| `ResultMethodCallNode` | `receiver, method_name, arg` | `.bachao(fallback)` / `.lazmi(msg)` |
| `GhaltiNode` | `message` | `ghalti(message)` statement form |

> Note: the old `PrintNode` / `MatchNode` / `KharabiNode` were removed. Printing is a builtin call; `match` is a reserved keyword with no syntax yet.

## Types

| Node | Fields | Description |
|------|--------|-------------|
| `TypeCastNode` | `target_type, expr` | `adad(x)`, `lafz(y)`, … |

<div class="recap">
<p>32 node classes total. The resolver stamps <code>hints</code> (slot index, scope level, inferred type) onto the nodes that need them; the compiler reads only those nodes plus literal structure.</p>
</div>