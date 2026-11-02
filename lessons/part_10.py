"""Part 10: Validate Generated Code as Untrusted Data. Run from repo root with python3 -m lessons.part_10."""
import json
from workbench.labs import lab

if __name__ == "__main__":
    print(json.dumps(lab(10), indent=2))
