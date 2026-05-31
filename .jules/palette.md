## 2024-05-31 - Mobile duplicate menu accessibility
**Learning:** When adding ARIA labels to UI components that have identical counterparts hidden in responsive modes (e.g., desktop vs mobile theme toggles), existing tests using `getByRole` may fail by finding multiple matches.
**Action:** Update such tests to handle multiple matches (e.g., using `getAllByRole("button")[0]`).
