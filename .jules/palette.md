## 2024-06-18 - Tailwind UI keyboard focus for visually hidden inputs
**Learning:** When styling custom radio buttons where the `<input type="radio">` is visually hidden (e.g., with `.sr-only`), keyboard focus on the input doesn't show a visible ring unless specifically handled.
**Action:** Apply Tailwind v4 `has-[:focus-visible]:ring-*` classes to the parent `<label>` element to ensure keyboard focus states remain visible when navigating via keyboard.
