## 2024-08-29 - Absolute-positioned Icon-only Buttons Lack Focus & Tooltips
**Learning:** In this Tailwind UI stack, absolute-positioned icon-only buttons (like the show/hide password toggle) inherently lack native focus visibility and mouse hover context, presenting an accessibility barrier for keyboard navigation and mouse users.
**Action:** Always explicitly attach `focus-visible:ring-2`, `focus-visible:outline-none`, rounding classes, and `title` attributes to custom interactive elements, especially absolute-positioned buttons.
