## 2024-05-15 - [Accessible Icon Buttons]
 **Learning:** In Tailwind projects, absolute-positioned icon-only buttons (like password toggles) lose default browser outlines due to preflight and often lack tooltip context for mouse users.
 **Action:** Always explicitly add `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary rounded-xl` classes and `title` attributes (matching the `aria-label`) to ensure both keyboard navigation visibility and mouse tooltips.
