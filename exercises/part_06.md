# Part 06 — Turn Expertise into a Reviewed Skill Contract

Add a documentation skill to the catalog without granting write access. Show that selecting it cannot fall through into pricing generation.

เพิ่ม skill ด้านเอกสารใน catalog โดยไม่ให้สิทธิ์เขียน แล้วพิสูจน์ว่าเลือก skill นี้ไม่ไหลไปสร้างโค้ดราคา

Run `python3 -m workbench.lesson 6`.

Target test: `test_semantic_review_cannot_generate` in `tests/test_boundaries.py`.

Keep input, actual state/reason and your explanation. The test protects a boundary; do not weaken policy to force a pass.

Expected architectural change: Unsupported skills stop; host capabilities remain explicit.

See [the lesson](https://anirach.com/blog/ai-engineering-skills.html).
