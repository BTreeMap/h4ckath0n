## 2024-05-24 - Keyboard accessibility for hover-only actions
 **Learning:** Elements hidden with `opacity-0` and revealed on hover (`group-hover:opacity-100`) must also include `focus-visible:opacity-100` or `group-focus-within:opacity-100` so that keyboard users can tab to them and see them.
 **Action:** Always include keyboard focus variants when using hover-based visibility classes.
