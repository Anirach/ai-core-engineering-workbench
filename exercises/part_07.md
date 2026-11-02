# Part 07 — Inspect Meaning Without Promoting Text into Authority

Add one benign quotation of an injection phrase and one mixed-language attack to a separate evaluation file. Do not tune against your held-out cases.

เพิ่มข้อความอ้างคำโจมตีในบริบทปกติหนึ่งกรณี และการโจมตีปนภาษาหนึ่งกรณีไว้ในชุดวัดแยก ห้ามปรับ threshold จาก held-out

Run `python3 -m workbench.lesson 7`.

Target test: `test_semantic_review_cannot_generate` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Suspicious or uncertain meaning routes to review.

See [the lesson](https://anirach.com/blog/ai-engineering-semantic-input.html).
