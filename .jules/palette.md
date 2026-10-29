## 2024-10-29 - Missing visual required indicators
 **Learning:** Forms with required fields weren't visually indicating to users that the field is mandatory, only relying on the semantic `required` prop which screen readers catch but visual users might miss until they submit.
 **Action:** Add a red asterisk `*` to `Input` and `PasswordField` components when the `required` prop is present so users know a field is required before form submission.
