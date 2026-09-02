## 2024-05-14 - Keyboard Accessibility for Icon-only Buttons
**Learning:** In Tailwind projects, absolute-positioned icon-only buttons (like password visibility toggles) often lose default focus outlines due to preflight, rendering them invisible to keyboard navigation. They also lack tooltips for mouse users.
**Action:** Always explicitly add \`focus-visible:ring-2\` (and related classes) and \`title\` attributes to custom interactive elements.
