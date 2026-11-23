## 2024-05-15 - Required Field Indicators in Labels
**Learning:** Adding a nested required visual indicator (like an asterisk) to React component labels breaks `@testing-library/react` tests that use `getByLabelText` with exact string matches, as the text content is no longer a perfect match.
**Action:** Always update associated `getByLabelText` queries to use regular expressions (e.g., `getByLabelText(/Label Name/)`) when adding nested elements inside labels.
