# Part 12 — Give Output Quality Its Own Acceptance Gate

Write a correct candidate with a misleading deployment claim. Label it independently, then test whether the quality evaluator agrees.

เขียน candidate ถูกแต่ summary อ้าง deploy เกินจริง ให้คนติด label ก่อน แล้วค่อยวัดว่า evaluator เห็นตรงหรือไม่

Run `python3 -m workbench.lesson 12`.

Target test: `test_high_average_does_not_override_low_dimension` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: A weak explanation still fails its own gate.

See [the lesson](https://anirach.com/blog/ai-engineering-quality-gate.html).
