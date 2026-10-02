## 2026-06-21 - Accessible Loading States in Interactive Elements
**Learning:** When creating reusable UI components like Button that support loading states, simply disabling the button and showing a spinner is insufficient for screen readers.
**Action:** Always bind the loading prop to aria-busy on the interactive element and add aria-hidden="true" to the spinner icon to ensure the loading context is announced properly while hiding decorative elements.
