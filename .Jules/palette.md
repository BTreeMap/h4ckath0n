## 2024-05-18 - Added focus ring to password toggle button
 **Learning:** Absolute positioned interactive elements inside inputs (such as password visibility toggles) often miss native focus rings or inherit clipped bounds.
 **Action:** Always explicitly add focus ring styling (e.g., focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary) and appropriate border radius to these elements to ensure they are visible during keyboard navigation.
