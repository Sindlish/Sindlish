"""
Sindlish Language Interpreter — compatibility entry point.

Keep this module for running the interpreter straight from a source checkout
(e.g. ``python main.py run hello.sd``). The real CLI lives in
``interpreter.cli`` and is published as the ``sindlish`` console script.
"""

from interpreter.cli import main

if __name__ == "__main__":
    main()