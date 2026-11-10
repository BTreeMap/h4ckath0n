## 2024-05-23 - Visible Focus on Custom Hidden Radios
**Learning:** When styling custom radio buttons where the `<input type="radio">` is visually hidden (e.g., with `.sr-only`), keyboard focus states become invisible. Tailwind v4's `has-[:focus-visible]:ring-*` classes must be applied to the parent `<label>` element to ensure keyboard focus remains visible.
**Action:** Always apply `has-[:focus-visible]:...` styling to the parent label when hiding native inputs using `.sr-only`.
