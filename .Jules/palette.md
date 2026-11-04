## 2023-10-25 - Required Field Indicators and Screen Readers
**Learning:** When adding visual indicators like asterisks (*) to form labels to denote required fields, screen readers will redundantly announce "star" or "asterisk" if the input already uses the semantic HTML `required` attribute.
**Action:** Always wrap decorative label indicators in a `span` with `aria-hidden="true"` within this design system's form primitives (e.g., `Input`, `PasswordField`) to preserve a clean auditory experience while maintaining visual clarity.
