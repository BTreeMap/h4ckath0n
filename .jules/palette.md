## 2024-05-24 - Visual indicator for required fields
**Learning:** Reusable input components (like `Input` and `PasswordField`) map the native `required` HTML prop to internal logic, but they lacked a visual indicator (like an asterisk) in the label to communicate this requirement to the user, creating a poor user experience.
**Action:** When a form field is required, display a visual indicator (like an asterisk) and ensure it has `aria-hidden="true"` so that screen readers don't announce it redundantly (since the input element itself will already have `required` mapped and announced).
