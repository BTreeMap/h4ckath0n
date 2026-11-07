## 2023-11-07 - Accessible Custom Radio Buttons
 **Learning:** When styling custom radio buttons where the `<input type="radio">` is visually hidden (e.g., with `.sr-only`), keyboard focus states become invisible.
 **Action:** Apply Tailwind v4 `has-[:focus-visible]:ring-*` classes to the parent `<label>` element to ensure keyboard focus states remain visible.
