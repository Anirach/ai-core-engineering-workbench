# Part 04 — Validate Inputs Before Spending Intelligence

Add a boundary case with Thai text and a byte length just above the limit. Confirm no provider call occurs.

เพิ่มกรณีข้อความไทยที่มี byte เกินขอบเขตเล็กน้อย แล้วตรวจว่า provider ไม่ถูกเรียก

Run `python3 -m workbench.lesson 4`.

Target test: `test_input_stops_before_inference` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: The request is rejected with zero provider calls.

See [the lesson](https://anirach.com/blog/ai-engineering-input-checks.html).
