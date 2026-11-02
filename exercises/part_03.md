# Part 03 — Make the Workflow a Typed State Machine

Draw the rejected, reviewed and revised exits for your current AI handler. Check that rejected runs cannot expose an accepted artifact.

วาดทางออก reject, review, revise ของ handler ที่ใช้อยู่ และตรวจว่างานไม่ผ่านไม่สามารถส่ง artifact แบบยอมรับแล้ว

Run `python3 -m workbench.lesson 3`.

Target test: `test_accept_still_has_zero_effects` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Every exit has a state, reason and stage trace.

See [the lesson](https://anirach.com/blog/ai-engineering-contracts.html).
