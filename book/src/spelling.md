# The Spelling Standard

<div class="youarehere">📍 <strong>You are here:</strong> Part Zero · Settle In</div>

Every public Sindlish name passes through one letter map before it ships. This chapter is the reference card for that map ([SEP 80](https://github.com/Sindlish/Sindlish/issues/80), *Sindlish Naming & Romanization Standard*): how Sindhi letters romanize, how the implicit-vowel system renders, and how the audit's replacement table is applied.

## The letter map

Each Sindhi letter has exactly one lowercase mapping:

| Sindhi | Sindlish | Sindhi | Sindlish | Sindhi | Sindlish |
|--------|----------|--------|----------|--------|----------|
| ا / آ  | a        | ذ      | z        | ع      | (carrier) |
| ب      | b        | ر      | r        | غ      | gh        |
| ٻ      | bb       | ڙ      | rr       | ف      | f         |
| ڀ      | bh       | ز      | z        | ق      | q         |
| پ      | p        | ژ      | zh       | ڪ / ک | k         |
| ڦ      | ph       | س / ث / ص | s     | گ      | g         |
| ت / ط  | t        | ش      | sh       | ڳ      | gg        |
| ٿ      | th       | ض / ظ  | z        | ڱ      | ng        |
| ٽ      | tt       | ح / ه / ھ | h     | ل      | l         |
| ٺ      | tth      | خ      | kh       | م      | m         |
| ج      | j        | د      | d        | ن      | n         |
| ڄ      | jj       | ڌ      | dh       | ڻ      | nn        |
| جھ     | jh       | ڏ / ڊ  | dd       | و      | w / u / o |
| ڃ      | ny       | ڍ      | ddh      | ي / ئ | y / i / e |
| چ      | ch       |        |          | ء      | (carrier) |
| ڇ      | chh      |        |          |        |           |

**Collapsed pairs** (distinct letters, one pronunciation, one spelling): `ا/آ`→`a`, `س/ث/ص`→`s`, `ض/ظ/ز/ذ`→`z`, `ت/ط`→`t`, `ح/ه/ھ`→`h`, `ڪ/ک`→`k`, `ڏ/ڊ`→`dd`, `ي/ئ`→`y`. No apostrophe is ever a valid identifier character.

## Rendering rules

- **Implicit vowels.** Sindhi writes short vowels diacritically; romanization supplies them from the natural pronunciation: `a`, `i`, `e`, `o`, `u`. Long/short length is **not** marked (`jari`, `wapas`, not `jaari`).
- **ي / و as vowels.** Terminal و reads as `o`/`u` (`majmuo`, `silsilo`); جي reads as `ji` (`jistain`, `bahari`). Root consonant ي is `y` (`ya`).
- **ع / ء carriers.** Word-initial they render the carried vowel and vanish (`adad`); medial they drop entirely (`majmuo`, `aalmi`).
- **Consonants strict, vowels lenient.** A name is re-spelled only when its *consonants* violate the map; vowel letters are never audited.

## English-origin replacements (SEP 80)

Names whose consonants were fine but whose *source word* was English were replaced outright — the old name is rejected, no alias:

| Old | New | Script | Meaning |
|---|---|---|---|
| `index` | `jaga` | جڳهه | *place / position* |
| `update` (lughat & majmuo) | `milap` | ميلاپ | *union / joining* |
| `addkar` | `shamil` | شامل | *include* |
| `symmetric_farq` | `bahamifarq` | باهمي فرق | *mutual difference* |
| `IndexJeGhalti` | `JagaJeGhalti` | جڳهه جي غلطي | *position-mistake* |
| `likh(sep=)` | `likh(vich=)` | وچ ۾ | *between* |
| `likh(end=)` | `likh(akhir=)` | آخِر | *end* |

`defaultrakh` (setdefault) is the one **retained** English-origin name: the SLA dictionary glosses "default" as negligence/fault (غفلت, خطا) with no usable native term, so the name survives as a registered exception. `ok` (Result), `match` (retired by work in #70) and `_` (wildcard) are the other retained exceptions.

## Where the map is enforced

Registered method names are produced from type `_methods` keys — tooling consumes the registry directly for the grammar and completions, so a rename in `collections.py` propagates to `vscode-extension/syntaxes/*.json` via `tools/generate_grammar.py`. Error classes keep the same internal machinery (`ERROR_MAP`); only their public spelling changes. User programs are **advisory**: the standard recommends, the compiler never enforces.

<div class="recap">
<p>One letter map, applied to every shipped name.</p>
<p>Consonants decide; vowels follow pronunciation.</p>
<p>English-origin tokens were replaced outright, not aliased.</p>
</div>