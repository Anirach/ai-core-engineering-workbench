"""Part 12: Give Output Quality Its Own Acceptance Gate. Run from repo root with python3 -m lessons.part_12."""
import json
from workbench.labs import lab

if __name__ == "__main__":
    print(json.dumps(lab(12), indent=2))
