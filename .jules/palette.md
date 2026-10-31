## 2024-11-20 - Nested elements in Labels breaks getByLabelText
 **Learning:** When adding nested elements like visual required indicators (e.g. asterisks) inside label elements in React, exact string matching in `@testing-library/react` tests utilizing `getByLabelText("Label")` will start failing due to the extra text content.
 **Action:** Update `getByLabelText` calls to use regular expressions, such as `getByLabelText(/Label/)`, instead of exact string matches to account for nested textual indicators inside labels.
