# Part 14 — Measure Outcomes Without Confusing Fixtures with Evidence

Design a held-out set with language and task slices. Write the coverage and accepted-error formulas, including the zero-accepted case.

ออกแบบ held-out ที่แยกภาษาและชนิดงาน เขียนสูตร coverage กับ accepted error รวมกรณีไม่มีงานผ่านเลย

Run `python3 -m workbench.lesson 14`.

Target test: `test_fixtures_do_not_claim_model_accuracy` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Architecture tests and live evidence are reported separately.

See [the lesson](https://anirach.com/blog/ai-engineering-evaluation.html).
