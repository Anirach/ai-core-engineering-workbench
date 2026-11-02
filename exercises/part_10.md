# Part 10 — Validate Generated Code as Untrusted Data

Try a decorator, a function-call default and a traversal path. Explain which independent check rejects each case.

ลอง decorator, default argument ที่เป็น function call และ path traversal อธิบายว่าด่านใดปฏิเสธแต่ละกรณี

Run `python3 -m workbench.lesson 10`.

Target test: `test_output_disallows_executable_python_features` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Imports, calls and unauthorized paths stop as data.

See [the lesson](https://anirach.com/blog/ai-engineering-output-checks.html).
