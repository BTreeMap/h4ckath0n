## 2024-09-04 - Missing Focus Outlines on Absolute Icon Buttons
 **Learning:** In this Tailwind-based design system, absolute-positioned icon-only interactive elements (like the password visibility toggle) lose browser default outlines due to preflight and can become completely invisible to keyboard navigators tabbing through forms.
 **Action:** Always explicitly apply `focus-visible:ring-2 focus-visible:outline-none` and a `title` attribute to icon-only buttons, especially when placed over inputs.
