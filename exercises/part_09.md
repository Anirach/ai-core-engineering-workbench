# Part 09 — Treat Context as a Versioned Software Dependency

Change one requirement sentence and show the context hash changes. Decide which behavior tests must change and which must stay invariant.

แก้ requirement หนึ่งประโยคและแสดงว่า context hash เปลี่ยน แล้วระบุ behavior test ที่ต้องแก้และข้อกำหนดที่ต้องคงเดิม

Run `python3 -m workbench.lesson 9`.

Target test: `test_reproducible_manifest` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: A changed evidence snapshot changes the run identity.

See [the lesson](https://anirach.com/blog/ai-engineering-context.html).
