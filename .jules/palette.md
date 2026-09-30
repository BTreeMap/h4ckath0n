## 2024-10-24 - Asterisks in Labels Break Testing Library String Queries
 **Learning:** When appending a visual indicator like an asterisk `*` inside a `<Label>` component, even if marked with `aria-hidden="true"`, React Testing Library's `getByLabelText("Label")` will fail because it looks for an exact string match which now includes the asterisk.
 **Action:** Always update affected tests to use regex queries (e.g., `getByLabelText(/Label/i)`) when modifying label text contents to avoid breaking the test suite.
