## 2024-05-18 - Visual Indicators for Required Fields
 **Learning:** In reusable form components (e.g., `Input`, `PasswordField`), adding a visual indicator (like an asterisk) inside the `<Label>` element breaks React Testing Library's exact string matches for `getByLabelText`, even if marked `aria-hidden="true"`.
 **Action:** Update affected tests to use regex matches (e.g., `getByLabelText(/Label/i)`) and always ensure the visual indicator has `aria-hidden="true"` to prevent redundant screen reader announcements.
