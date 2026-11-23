## 2024-11-06 - Visual Required Indicators Break Exact Label Text Matches
 **Learning:** Adding nested visual elements like asterisks (`<span aria-hidden="true">*</span>`) inside label components breaks `@testing-library/react` tests that use `getByLabelText("Exact String")`.
 **Action:** Update associated tests to use regular expressions like `getByLabelText(/Exact String/)` instead of strict string matching to prevent CI test failures when enhancing labels with nested visual indicators.
