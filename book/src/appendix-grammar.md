# Appendix: Grammar (EBNF)

<div class="youarehere">📍 <strong>You are here:</strong> Appendix · Reference</div>

The full concrete grammar of Sindlish, as implemented by `interpreter/frontend/parser.py`. `match` is reserved as a keyword but has no production yet; printing is a builtin call, so there is no `print` statement.

```ebnf
program     = statement* EOF

statement   = if_stmt
            | while_stmt
            | for_stmt
            | func_def
            | return_stmt
            | break_stmt
            | continue_stmt
            | assignment
            | block
            | global_decl
            | nonlocal_decl
            | expression

expression  = or
or          = and ("ya" and)*
and         = not ("aen" not)*
not         = "nah" not | comparison
comparison  = term (("==" | "!=" | ">" | "<" | ">=" | "<=") term)*
term        = factor (("+" | "-") factor)*
factor      = power (("*" | "/" | "%") power)*
power       = unary ("^" power)?               (* right-associative *)
unary       = ("-" | "nah") unary | postfix
postfix     = primary ("?" | "!!" | "." ident | "[" expr "]" | "(" args ")")*

primary     = NUMBER | STRING | BOOL | NULL
            | IDENT
            | "(" expression ")"
            | list | dict | set
            | type_cast | result_ctor

list        = "[" (expression ("," expression)*)? "]"
dict        = "{" (expr ":" expr ("," expr ":" expr)*)? "}"
set         = "{" (expression ("," expression)*)? "}"

func_def    = "kaam" IDENT "(" params ")" ("->" type)? block
params      = (param ("," param)*)?
param       = ("*" | "**")? type? IDENT (":" type)? ("=" expression)?

if_stmt     = "agar" expression block ("yawari" expression block)* ("warna" block)?
while_stmt  = "jistain" expression block
for_stmt    = "har" IDENT "mein" expression block
block       = "{" statement* "}"

return_stmt = "wapas" expression?
break_stmt  = "tor"
continue_stmt = "jari"
global_decl = "aalmi" IDENT
nonlocal_decl = "bahari" IDENT

assignment  = "pakko"? type? IDENT (":" type)? "=" expression
            | IDENT (":" type)? "=" expression
            | type? IDENT "[" type ("," type)? "]" "=" expression   (* typed collections *)

type        = "adad" | "lafz" | "dahai" | "faislo" | "khali"
            | "pakko" | "fehrist" | "lughat" | "majmuo" | "kaam"
type_cast   = type "(" expression ")"
result_ctor = ("ok" | "ghalti") "(" expression? ")"
```

## Token inventory

`TokenType` (in `interpreter/frontend/tokens.py`) has **57 members**, grouped as:

- **Types & literals (13):** `ADAD LAFZ DAHAI FAISLO SACH KOORE KHALI PAKKO FEHRIST LUGHAT MAJMUO KAAM IDENTIFIER`
- **Control keywords (14):** `AGAR YAWARI WARNA JISTAIN BAHARI AALMI WAPAS MATCH OK GHALTI HAR TOR JARI MEIN`
- **Operators (16):** `PLUS MINUS MUL DIV MOD POW GT LT EQ EQEQ NOTEQ GTEQ LTEQ AND OR NOT QMARK BANGBANG DBLSTAR`
- **Symbols (10):** `LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET COLON COMMA DOT NEWLINE EOF`

> `LIKH` and `KHARABI` were removed from the enum; `likh` is an identifier resolved to the builtin, and panics use `! !` / `lazmi()`.

<div class="recap">
<p><code>KEYWORDS</code> maps 29 Sindhi words to TokenTypes; <code>DATATYPES</code> lists the 8 annotation types (<code>ADAD LAFZ DAHAI FAISLO KHALI FEHRIST LUGHAT MAJMUO</code>).</p>
</div>