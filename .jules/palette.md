## 2025-03-09 - Nested label elements break exact-match testing queries
**Learning:** When adding a nested required indicator asterisk to an existing label, it breaks `@testing-library/react` tests utilizing `getByLabelText("Exact Label Name")` due to exact string matching failing against the combined textual content (e.g., "Email *").
**Action:** Always update associated component and integration tests to use regular expression matchers (`getByLabelText(/Exact Label Name/)`) when adding visually appended indicators to labels.
