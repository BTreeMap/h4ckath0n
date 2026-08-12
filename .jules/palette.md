## 2025-05-22 - Add keyboard focus indicator to visually hidden theme radio buttons
**Learning:** When using Tailwind's `sr-only` to visually hide native `<input type="radio">` elements, the browser's default keyboard focus indicator is lost. This makes it impossible for keyboard users to see which option is currently focused.
**Action:** Always apply `has-[:focus-visible]:ring-2` (or similar focus ring utilities) to the visible parent wrapper (e.g., `<label>`) of visually hidden inputs to ensure keyboard focus indicators are preserved and displayed around the visible component.
