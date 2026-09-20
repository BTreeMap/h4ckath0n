## 2024-05-20 - [Added visual indicators for required form fields]
 **Learning:** React Testing Library's exact string matches for `getByLabelText` fail when appending an `aria-hidden` required asterisk inside the `<Label>` component. The appended text alters the full label text, even though it is hidden from screen readers.
 **Action:** When adding visual indicators like an asterisk to labels, update affected tests to use regex matches (e.g., `getByLabelText(/Label/i)`) instead of exact string matches.
