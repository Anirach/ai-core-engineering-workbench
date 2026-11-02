# Part 01 — From Writing Every Branch to Engineering Decisions

Write a success contract for one feature you currently implement by hand. List three exact rules and one judgment that needs a model.

เขียนสัญญาความสำเร็จของ feature ที่ทำอยู่ ระบุกฎที่ตรวจแน่นอนได้สามข้อ และการตีความที่ควรใช้โมเดลหนึ่งข้อ

Run `python3 -m workbench.lesson 1`.

Target test: `test_shape_does_not_imply_behavior` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: A wrong implementation is held for review.

See [the lesson](https://anirach.com/blog/ai-engineering-old-to-new.html).
