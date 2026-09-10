import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from interpreter import Interpreter
from interpreter.errors import SindhiBaseError


def lint(file_path):
    try:
        code = Path(file_path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as e:
        print(f"1:Error reading file {e}")
        return 1

    try:
        Interpreter().check(code)
    except SindhiBaseError as e:
        print(f"{e.line}:{e}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/lint.py <file.sd>")
        sys.exit(2)
    sys.exit(lint(sys.argv[1]))