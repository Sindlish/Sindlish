# Sindlish Programming Language

[![CI](https://github.com/Sindlish/Sindlish/actions/workflows/ci.yml/badge.svg)](https://github.com/Sindlish/Sindlish/actions/workflows/ci.yml)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

Sindlish is a high-level, full-featured programming language designed specifically for the Sindhi-speaking communities. It provides a familiar native-language experience while maintaining a robust, modern syntax and a high-performance bytecode virtual machine backend.

## Overview

For decades, the programming world has been heavily dominated by the English language. This creates an unnecessary barrier to entry for millions of talented individuals who think and speak in Sindhi or Urdu. Sindlish breaks that barrier, allowing developers to write professional software using the words they already know natively.

## Key Features

- **Native Keywords**: Utilize words like `kaam` (function), `agar` (if), `lafz` (string), `adad` (integer), and `faislo` (boolean).
- **Hybrid Typing System**: Supports both dynamic typing and static type annotations for robust software development.
- **Modern Collections**: Built-in support for lists (`fehrist`), dictionaries (`lughat`), and sets (`majmuo`).
- **Crash-Proof Error Handling**: Employs a Result system instead of traditional try/catch mechanisms, allowing safe unwrapping of values using soft fallbacks and explicit panics.
- **Bytecode Virtual Machine**: Fast and efficient execution environment.

## Installation

You can install Sindlish via the provided installer for macOS/Linux or directly run it using Python.

### Quick Start

Run the interpreter interactively:
```bash
uv run main.py            # from a source checkout
uv run sindlish repl      # when installed as a console script
```

Execute a file:
```bash
uv run main.py run script.sd
```

Try the bundled examples in [`examples/`](examples/):
```bash
uv run main.py run examples/hello.sd
```

Access offline documentation from the terminal:
```bash
uv run main.py docs
```

## Roadmap & Planning

All forward work is tracked as GitHub issues grouped under
[**milestones**](https://github.com/Sindlish/Sindlish/milestones). The narrative
roadmap lives in [`roadmap/ROADMAP.md`](roadmap/ROADMAP.md). Ideas, questions,
and discussion are welcome in [GitHub Discussions](https://github.com/Sindlish/Sindlish/discussions).

## Documentation

The canonical documentation is the mdBook in [`book/`](book/) (*Sindlish Internals — A Cozy Field Guide*). Build it locally with `mdbook build book`. The older `docs/` website and `developer-docs/` were removed from the repo; the language reference and walkthroughs all live in the book.

## License

Sindlish is free software, released under the [GNU General Public License, version 3 or (at your option) any later version](LICENSE) (`SPDX: GPL-3.0-or-later`). You can redistribute it and/or modify it under its terms — see the full text in [`LICENSE`](LICENSE) and the copy that ships inside the VS Code extension in [`vscode-extension/LICENSE`](vscode-extension/LICENSE).

Copyright (C) 2026 Amanat Ali Panhwer

Contributions are governed by our [Code of Conduct](CODE_OF_CONDUCT.md).
