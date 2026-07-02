## 2024-05-27 - Added responsive accessibility
**Learning:** Adding ARIA labels to UI components that have identical counterparts hidden in responsive modes (e.g., desktop vs mobile theme toggles) can cause tests using `getByRole` to fail by finding multiple elements.
**Action:** Update such tests to handle multiple matches (e.g., using `getAllByRole(...)[0]`).
