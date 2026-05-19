
## 2024-05-19 - Duplicate Accessible Elements Break Strict Queries
 **Learning:** When adding ARIA labels to UI components that have identical counterparts hidden in responsive modes (e.g., desktop vs mobile theme toggles), standard test assertions relying on `getByRole` expecting a unique match will fail due to finding multiple elements.
 **Action:** Update test assertions using `getAllByRole` indexed explicitly, and always consider how visually responsive identical components surface to screen readers and test frameworks.
