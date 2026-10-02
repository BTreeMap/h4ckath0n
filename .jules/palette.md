## 2024-05-18 - Preserve keyboard focus indicators on custom radio buttons with sr-only inputs
**Learning:** When using Tailwind's `sr-only` to visually hide native inputs (e.g., in custom radio buttons), the focus ring is lost, severely hurting keyboard accessibility.
**Action:** Always apply `has-focus-visible:` or `has-[:focus-visible]:` utility classes (e.g., `has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-primary has-[:focus-visible]:ring-offset-2`) to the visible parent wrapper (e.g., `<label>`) to ensure keyboard focus indicators are preserved.
