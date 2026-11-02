# Part 02 — Keep a Functional Core Around a Fallible Model

Move an existing permission check into a pure function. Test two principals against the same model response.

ย้ายการตรวจสิทธิ์เดิมเป็น pure function แล้วทดสอบผู้ใช้สองสิทธิ์กับ response โมเดลชุดเดียวกัน

Run `python3 -m workbench.lesson 2`.

Target test: `test_permission_stops_before_inference` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Policy can be replayed and tested without the provider.

See [the lesson](https://anirach.com/blog/ai-engineering-functional-core.html).
