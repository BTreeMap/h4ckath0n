## 2024-05-24 - Visual Required Indicator

 **Learning:** Mapped the native `required` prop on Input and PasswordField components to a visual asterisk `*` in the Label. To keep it accessible, I made sure to apply `aria-hidden="true"` to the asterisk so it won't be redundantly read aloud by screen readers since the native `required` attribute is already handling accessibility.

 **Action:** For all reusable form components, map validation props (`required`, `optional`, etc.) to clear visual indicators but keep them hidden from screen readers.
