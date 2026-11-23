## YYYY-MM-DD - Required Field Visual Indicators
**Learning:** When modifying React component labels to include nested visual indicators (such as an asterisk for required fields), update associated `@testing-library/react` tests that use `getByLabelText` with exact string matches to use regular expressions (e.g., `getByLabelText(/Label Name/i)`) to prevent CI test failures.
**Action:** Always check test files for exact string label queries when updating label DOM structure.
