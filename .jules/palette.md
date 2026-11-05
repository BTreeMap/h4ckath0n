## 2026-11-05 - Focus rings on custom radio buttons
 **Learning:** When styling custom radio buttons where the `<input type="radio">` is visually hidden (e.g., with `.sr-only`), the focus state is lost.
 **Action:** Apply Tailwind v4 `has-[:focus-visible]:ring-*` classes to the parent `<label>` element to ensure keyboard focus states remain visible.
