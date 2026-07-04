## 2025-03-01 - Add busy and expanded ARIA properties to base UI
 **Learning:** Base interactive components (like generic buttons or nav menus) missing `aria-busy` or `aria-expanded` leave screen-reader users without feedback on async state and structure, causing confusion in multi-step flows.
 **Action:** Enforce `aria-busy={isLoading}` and `aria-live="polite"` in Button/Icon wrappers, and `aria-expanded={isOpen}` in toggleable layouts.
