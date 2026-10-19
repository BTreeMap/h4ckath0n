## 2026-10-19 - [Visual indicators on component labels]
 **Learning:** Added decorative visual indicators to component labels for required fields (using `*`) along with `aria-hidden="true"`. This prevents screen readers from reading the symbol aloud, relying on standard semantic HTML attributes.
 **Action:** Make sure to always include `aria-hidden="true"` on non-semantic decorative textual indicators in UI components.
