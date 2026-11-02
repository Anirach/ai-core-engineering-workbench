import argparse
import json
from .labs import lab


def main():
    p = argparse.ArgumentParser(description="Offline architecture lessons; makes no API calls")
    p.add_argument("part", help="1..15, or all")
    a = p.parse_args()
    parts = range(1, 16) if a.part == "all" else [int(a.part)]
    for n in parts:
        print(json.dumps({"part": n, "result": lab(n)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
