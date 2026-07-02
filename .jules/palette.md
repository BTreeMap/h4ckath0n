## 2024-05-09 - [Icon Button Tooltips]
**Learning:** Found multiple icon-only buttons (like the theme toggler and mobile menu in `Layout.tsx`, and visibility toggle in `PasswordField.tsx`) that lack visual tooltips explaining their function. While they have ARIA labels for screen readers, sighted users don't get hover feedback about what the button does.
**Action:** Always consider adding `title` attributes (or a Tooltip component) to icon-only buttons to improve discoverability for sighted mouse users.
