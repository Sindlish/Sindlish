"""
Sindlish Interpreter — Public API.

Provides the Interpreter facade class that encapsulates the full
pipeline: lex → parse → resolve → compile → execute.

The facade exposes each stage as a separate method so consumers can
stop at any point in the pipeline (checking, tooling, testing) without
re-implementing stage wiring themselves.
"""

import sys

from .analysis.resolver import Resolver
from .backend.compiler import Compiler
from .backend.vm import VM
from .errors import ErrorReporter, SindhiBaseError
from .frontend.lexer import Lexer
from .frontend.parser import Parser
from .frontend.tokens import TokenType
from .runtime.builtins import SimpleBuiltins
from .runtime.env import Environment

__version__ = "0.1.1"


def get_version() -> str:
    """Return the installed package version, falling back to the source version."""
    try:
        from importlib.metadata import PackageNotFoundError, version

        return version("sindlish")
    except PackageNotFoundError:
        return __version__


class Interpreter:
    """
    High-level facade for running Sindlish source code.

    Usage:
        interp = Interpreter()
        interp.run_source(code_string)
    """

    def __init__(self, globals_env: Environment | None = None):
        self._globals_env = globals_env if globals_env is not None else self.create_globals_env()

    @staticmethod
    def create_globals_env() -> Environment:
        """Create and populate the global environment with built-in functions."""
        globals_env = Environment()
        simple_handler = SimpleBuiltins()
        for name, func in simple_handler.get_all().items():
            globals_env.define(name, value=func, var_type=TokenType.KAAM, is_const=True)
        return globals_env

    # ---- Pipeline stages --------------------------------------------------

    def lex(self, code: str) -> list:
        """Stage 1: tokenize source code."""
        return Lexer(code).generate_tokens()

    def parse(self, tokens: list, code: str):
        """Stage 2: build the AST from tokens."""
        return Parser(tokens, code).parse()

    def resolve(self, ast, code: str) -> Resolver:
        """Stage 3: resolve names/types; stamps slot metadata onto the AST."""
        resolver = Resolver(code)
        resolver.resolve(ast)
        return resolver

    def compile(self, ast, code: str):
        """Stage 4: lower the AST to bytecode."""
        return Compiler(code).compile(ast)

    def build_vm(self, code, instructions, constants, line_col_map, ast, resolver) -> VM:
        """Package compiled output into a ready-to-run VM."""
        return VM(
            code,
            instructions,
            constants,
            self._globals_env,
            getattr(ast, "slot_count", 0),
            resolver.slot_metadata,
            line_col_map,
        )

    def check(self, code: str) -> None:
        """
        Run lex → parse → resolve → compile without executing.

        Raises SindhiBaseError on any lexical, syntactic, or semantic error.
        """
        tokens = self.lex(code)
        ast = self.parse(tokens, code)
        self.resolve(ast, code)
        self.compile(ast, code)

    def run_source(self, code: str, is_repl: bool = False) -> VM:
        """
        Run Sindlish source code through the full pipeline.

        Returns the VM instance after execution (for inspection/testing).
        In REPL mode errors are re-raised; otherwise the process exits(1).
        """
        try:
            tokens = self.lex(code)
            ast = self.parse(tokens, code)
            resolver = self.resolve(ast, code)
            instructions, constants, line_col_map = self.compile(ast, code)
            vm = self.build_vm(code, instructions, constants, line_col_map, ast, resolver)
            vm.run()
            return vm
        except SindhiBaseError as e:
            ErrorReporter.report(e)
            if not is_repl:
                sys.exit(1)
            raise
        except Exception as e:
            print(f"Internal Error: {e}")
            if not is_repl:
                sys.exit(1)
            raise


__all__ = ["Interpreter", "__version__", "get_version"]