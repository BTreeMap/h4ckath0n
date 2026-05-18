## 2025-04-25 - Extracted shared parsing pipelines for strings

**Learning:** Comma-separated strings (like scopes) were being manually parsed and stripped across `cli.py` and `dependencies.py` using `.split(",")`, creating subtle inconsistencies when handling leading/trailing whitespaces around empty fields or building sets directly.
**Action:** When working with structured strings or list transformations, always abstract the logic into a pure FP-style data processing pipeline (`filter`, `map`) inside a central `scopes.py` module to preserve order determinism, guarantee uniform cleanup, and reduce duplicate logic across the backend.
