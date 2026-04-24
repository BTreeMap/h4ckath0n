
## 2026-04-24 - Keyboard focus visibility in hover-only and visually hidden inputs
**Learning:** Elements that rely on `group-hover:opacity-100` for visibility or use `sr-only` inputs inside labels lack visible focus indicators for keyboard users.
**Action:** Always include `focus-visible:opacity-100` alongside hover opacity, and use the `has-[:focus-visible]:ring-*` Tailwind pattern on the parent label for visually hidden inputs to ensure accessible keyboard navigation.
