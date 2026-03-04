## 2026-03-04 - Password Visibility Toggle
**Learning:** Adding a native visibility toggle to universal `Input.tsx` primitives rather than expecting developers to build them per-instance prevents inconsistent implementations and missing ARIA attributes.
**Action:** Always build common input behaviors (like password show/hide, clearability) directly into the lowest-level design system primitives so they inherit consistent accessibility logic out of the box.
