## 2024-05-18 - Missing keyboard focus on custom radios
**Learning:** When styling custom radio buttons where the `<input type="radio">` is visually hidden (e.g., with `.sr-only`), keyboard focus states are lost if not explicitly handled on the parent.
**Action:** Apply Tailwind v4 `has-[:focus-visible]:ring-*` classes to the parent `<label>` element to ensure keyboard focus states remain visible on the container.
