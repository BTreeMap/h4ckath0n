## 2023-10-24 - Test Selectors vs Design Additions
 **Learning:** When adding purely visual/UX elements like a required asterisk (`*`) inside a `Label` component, React Testing Library tests using `getByLabelText` with exact string matches (e.g. `getByLabelText("Email")`) will break because the text node now reads `"Email*"`.
 **Action:** Always update associated RTL queries to use regex matching (e.g. `getByLabelText(/Email/i)`) when modifying label components to include visual decorators, maintaining test resilience while improving UX.
