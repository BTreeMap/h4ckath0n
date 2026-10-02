## 2024-05-23 - Focus styles on absolute positioned input elements
**Learning:** Absolute positioned interactive elements inside inputs (such as password visibility toggles) often miss native focus rings or inherit clipped bounds.
**Action:** Always explicitly add focus ring styling (`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary`) and appropriate border radius (`rounded-xl`) to these elements to ensure they are visible during keyboard navigation.
