## 2024-11-03 - Dynamic Labels in Testing
**Learning:** When adding dynamic nested visual indicators (like an asterisk for required fields) to React component labels, it changes the `textContent` of the label, causing `@testing-library/react` tests that use `getByLabelText` with exact string matches to fail.
**Action:** Always update associated `getByLabelText` calls to use regular expressions (e.g., `getByLabelText(/Label Name/)`) instead of exact string matches when making dynamic visual changes to labels to prevent CI test failures.
