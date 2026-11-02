# Part 08 — Make Guardrails Enforceable at the Effect Boundary

Attempt a different repository, a guest principal and merge_main. Assert that all three stop before inference.

ลอง repository อื่น principal เป็น guest และ action merge_main แล้วตรวจว่าทั้งสามหยุดก่อน inference

Run `python3 -m workbench.lesson 8`.

Target test: `test_permission_stops_before_inference` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Forbidden actions have no authorized path or provider call.

See [the lesson](https://anirach.com/blog/ai-engineering-guardrails.html).
