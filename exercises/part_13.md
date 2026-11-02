# Part 13 — Bound Repairs, Retries and Failure Recovery

Set max_calls to zero, then force a permanent quality failure. Verify finite termination and that rejected drafts are not returned as accepted.

ตั้ง max_calls เป็นศูนย์ แล้วจำลอง quality failure ถาวร ตรวจว่าหยุดแน่นอนและไม่ส่งร่างที่ไม่ผ่านในสถานะยอมรับ

Run `python3 -m workbench.lesson 13`.

Target test: `test_bounded_repair` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: One revision succeeds or the workflow stops at review.

See [the lesson](https://anirach.com/blog/ai-engineering-bounded-repair.html).
