## 2024-05-12 - The sr-only Trap
 **Learning:** Custom UI components (like radio buttons) that visually hide the native `<input>` using Tailwind's `sr-only` will completely hide browser focus indicators from keyboard users.
 **Action:** Always use Tailwind's `has-[:focus-visible]:` or `has-focus-visible:` on the visible parent wrapper (e.g., `<label>`) when hiding native inputs to restore a visible focus state for keyboard navigation.
