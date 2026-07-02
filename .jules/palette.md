## 2024-06-01 - Responsive Navigation Accessibility
**Learning:** Adding ARIA labels to hidden responsive elements (like mobile theme toggles) causes tests using `getByRole` to fail due to multiple matches.
**Action:** When adding accessibility to responsive elements, always update tests to handle multiple matches using `getAllByRole("button")[0]` or similar techniques, and ensure a skip-to-content link exists to bypass repeated responsive nav structures.
