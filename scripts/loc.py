"""print loc in this project"""

import pathlib


def count_loc():
    total = 0
    for path in pathlib.Path(".").rglob("*.py"):
        if ".venv" not in path.parts:  # skip any file under .venv
            total += sum(1 for _ in open(path, encoding="utf-8"))
    return total


if __name__ == "__main__":
    total = count_loc()
    print(f"LOC: {total}")
