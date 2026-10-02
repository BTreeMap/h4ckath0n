## 2024-05-20 - Add focus and tooltip to absolute-positioned buttons
**Learning:** Tailwind's preflight removes default browser outlines. Absolute-positioned icon-only buttons (like the password toggle inside an input wrapper) often miss explicit `focus-visible` styles, leading to invisible keyboard focus states. They also need `title` attributes for sighted users as `aria-label` only helps screen readers.
**Action:** Always explicitly add `focus-visible:ring-2` and `title` attributes to custom interactive elements, especially absolute-positioned icon-only buttons.
