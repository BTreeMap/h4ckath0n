## 2024-10-18 - Visual Required Indicators
 **Learning:** When appending a visual indicator (like an asterisk) inside a `<Label>` element for required fields, React Testing Library's exact string matches for `getByLabelText` (e.g., `getByLabelText("Label")`) fail because it includes the appended text, even if marked `aria-hidden="true"`.
 **Action:** Apply `aria-hidden="true"` to visual required indicators to prevent redundant screen reader announcements, and update affected tests to use regex matches (e.g., `getByLabelText(/Label/i)`) instead of exact string matches.
