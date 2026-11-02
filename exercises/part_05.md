# Part 05 — Use Jev as a Typed Decision Dependency

Change one returned probability to NaN and then remove one label. Both must stop before generation. Next test a valid but uncertain answer.

เปลี่ยน probability เป็น NaN แล้วลองลบ label หนึ่งตัว ทั้งคู่ต้องหยุดก่อนสร้างร่าง จากนั้นทดสอบคำตอบรูปแบบถูกแต่ไม่แน่ใจ

Run `python3 -m workbench.lesson 5`.

Target test: `test_invalid_probability_rejected` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Malformed decisions stop; uncertainty has a review route.

See [the lesson](https://anirach.com/blog/ai-engineering-jev-decisions.html).
