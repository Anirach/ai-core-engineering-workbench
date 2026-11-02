# Part 15 — Release the Whole Workflow with Evidence and a Rollback

Write a shadow-release plan with owners, stop conditions and a rollback target. Identify every behavior-changing artifact your release must pin.

เขียนแผน shadow release ระบุเจ้าของ เงื่อนไขหยุด และรุ่นย้อนกลับ แล้วแจกแจง artifact ที่เปลี่ยนพฤติกรรมซึ่งต้องตรึง

Run `python3 -m workbench.lesson 15`.

Target test: `test_release_separate_from_runtime` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Release requires separate evidence; rollback stays available.

See [the lesson](https://anirach.com/blog/ai-engineering-release.html).
