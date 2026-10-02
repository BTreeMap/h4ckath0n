## 2024-09-27 - Mapping required prop to visual indicator
 **Learning:** In reusable form components, appending an asterisk element to a Label element causes exact string matches in React Testing Library's `getByLabelText` to fail, even if the appended element is marked `aria-hidden="true"`.
 **Action:** Always use regex matches (e.g. `getByLabelText(/Label/i)`) when writing tests for inputs that might include appended visual indicators like asterisks inside their label wrapper.
