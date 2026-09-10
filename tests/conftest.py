"""
Shared test helpers for Sindlish interpreter tests.

Provides run() to execute Sindlish code and helpers to extract values
from the VM for assertions.
"""

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from interpreter import Interpreter
from interpreter.objects import (
    SdBool,
    SdDict,
    SdList,
    SdNull,
    SdNumber,
    SdResult,
    SdSet,
    SdString,
)


def create_globals_env():
    return Interpreter.create_globals_env()


def run(code: str):
    """
    Run Sindlish source code end-to-end and return
    (vm_instance, captured_stdout).

    Routes through the Interpreter facade stages so tests exercise the
    exact same pipeline as the CLI and REPL.
    """
    interp = Interpreter(create_globals_env())

    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    try:
        tokens = interp.lex(code)
        ast = interp.parse(tokens, code)
        resolver = interp.resolve(ast, code)
        instructions, constants, line_col_map = interp.compile(ast, code)
        vm = interp.build_vm(code, instructions, constants, line_col_map, ast, resolver)
        vm.run()
    finally:
        sys.stdout = old_stdout

    return vm, buffer.getvalue()


def get_variable_value(vm, name):
    """
    Get variable value from VM instance.
    Prefers globals-environment records; falls back to main-frame slots.
    Extracts raw value from SdShey wrappers.
    """
    if name in vm.globals.records:
        return extract_value(vm.globals.records[name].value)

    frame = vm.frames[-1]
    if hasattr(vm, "slot_names") and name in vm.slot_names:
        slot_idx = vm.slot_names[name]
        if 0 <= slot_idx < len(frame.slots) and frame.slots[slot_idx] is not None:
            return extract_value(frame.slots[slot_idx])
    return None


def extract_value(sd_object):
    """
    Extract Python value from a SdShey for testing.
    Recursively converts SdSheys to native Python types.
    """
    if isinstance(sd_object, (SdNumber, SdString, SdBool)):
        return sd_object.value
    elif isinstance(sd_object, SdNull):
        return None
    elif isinstance(sd_object, SdList):
        return [extract_value(elem) for elem in sd_object.elements]
    elif isinstance(sd_object, SdDict):
        return {
            extract_value(k) if not isinstance(k, str) else k: extract_value(v)
            for k, v in sd_object.items()
        }
    elif isinstance(sd_object, SdSet):
        return {extract_value(elem) for elem in sd_object.elements}
    elif isinstance(sd_object, SdResult):
        if sd_object.is_ok():
            return extract_value(sd_object.value)
        return sd_object
    else:
        return sd_object
