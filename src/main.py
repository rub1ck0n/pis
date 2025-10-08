from __future__ import annotations
import sys, json
from pathlib import Path
from .pis_app.pipeline import process_lines

def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    # файл по аргументу, иначе stdin
    if argv:
        path = Path(argv[0])
        if not path.exists() or not path.is_file():
            sys.stderr.write(f"Файл не найден: {path}\n")
            return 2
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        lines = sys.stdin.read().splitlines()

    had_errors = False
    for obj in process_lines(lines):
        if obj.get("type") == "ERROR":
            had_errors = True
        print(json.dumps(obj, ensure_ascii=False))
    return 1 if had_errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
