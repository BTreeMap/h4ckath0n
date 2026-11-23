## 2024-11-11 - Accessible Custom Radio Buttons
**Learning:** When styling custom radio buttons where the `<input type="radio">` is visually hidden (e.g., with `.sr-only`), applying Tailwind v4 `has-[:focus-visible]:ring-*` classes to the parent `<label>` element ensures keyboard focus states remain visible.
**Action:** Always check keyboard navigation for custom inputs and use `has-[:focus-visible]` on the visible parent wrapper if the actual input is visually hidden.
