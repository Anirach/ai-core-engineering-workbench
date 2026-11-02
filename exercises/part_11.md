# Part 11 — Test Behavior Against an Independent Oracle

Create a formula that passes one visible example but fails a boundary case. Add a property that catches it without copying its implementation.

สร้างสูตรที่ผ่านตัวอย่างเดียวแต่ผิดกรณีขอบ แล้วเพิ่ม property ที่จับได้โดยไม่ลอก implementation มาสร้าง test

Run `python3 -m workbench.lesson 11`.

Target test: `test_shape_does_not_imply_behavior` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: An independent expected value catches the wrong formula.

See [the lesson](https://anirach.com/blog/ai-engineering-behavior-checks.html).
