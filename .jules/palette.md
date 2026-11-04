## 2024-10-25 - Ensure focus visibility for hover-revealed elements
**Learning:** Hiding interactive elements behind `opacity-0 group-hover:opacity-100` creates an accessibility trap where keyboard users tab to invisible elements.
**Action:** Always include `focus-visible:opacity-100` (or `group-focus-within:opacity-100`) when using hover-based visibility classes.
