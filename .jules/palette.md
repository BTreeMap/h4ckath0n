## 2024-06-17 - Bind loading to aria-busy and hide spinner from screen readers
 **Learning:** In React UI components with loading states, explicitly binding the loading prop (e.g., `isLoading`) to the `aria-busy` attribute on the interactive element and applying `aria-hidden="true"` to any inner decorative spinner icons ensures screen readers properly announce the loading context without reading out decorative elements.
 **Action:** Apply this pattern to all interactive elements with a loading state, like the `<Button />` component.
