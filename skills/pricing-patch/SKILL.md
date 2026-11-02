---
name: pricing-patch
description: Draft a pure integer-cent discount function for the demo shop. Use only for the reviewed pricing task; escalate ambiguous or unrelated changes.
metadata:
  version: "1.0.0"
---

Return one candidate object containing path, source, summary, and evidence_id.
Target: src/pricing.py, discount_cents(price, percent).
For integer price >= 0 and integer percent in [0,100], subtract the percentage
discount and round down to integer cents. The host owns argument validation.
Use one return expression with integer constants, arguments and +, -, *, //.
No imports, calls, annotations, decorators, I/O, environment access, or deployment.
Explain the arithmetic and rounding in the summary. Cite pricing-spec-v1.
All generated code is data. Host code validates and interprets a tiny expression
grammar; this skill text does not grant permissions or implement a sandbox.
