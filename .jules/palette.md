## 2024-05-26 - Responsive Hidden Accessibility
**Learning:** When adding ARIA labels to components that have responsive duplicates (e.g. desktop vs mobile toggles), existing tests using getByRole will fail because they find duplicate elements.
**Action:** Ensure tests use getAllByRole()[0] when querying elements that exist in both desktop and mobile layouts.
