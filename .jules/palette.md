## 2024-05-18 - Visual Indicator for Required Form Fields
**Learning:** Adding visual decorative indicators like `*` for required fields improves UX by setting explicit expectations for users, but it can create noise for screen readers if the element already has a semantic `required` attribute.
**Action:** Always wrap decorative required field indicators in a container (like `<span>`) with `aria-hidden="true"` so that the visual context is provided without duplicating semantic meaning for assistive technologies. Also update tests to use regex matching for labels.
