## 2024-05-18 - Visual Indicators for Required Fields
 **Learning:** When appending visual indicators (like an asterisk) inside a `<Label>` element for accessibility (`aria-hidden="true"`), React Testing Library's `getByLabelText("Label")` will fail because it looks for an exact string match which now includes the asterisk.
 **Action:** Always update associated unit tests to use regex matching (e.g., `getByLabelText(/Label/i)`) when altering label text content with decorative visual indicators.
