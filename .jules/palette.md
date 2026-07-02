## 2024-05-24 - Duplicate Responsive Controls A11y Testing
**Learning:** When ensuring mobile responsive UI elements (e.g. mobile vs desktop theme toggle buttons) have accessible names (`aria-label`), `getByRole` will fail in React Testing Library if the test assumes only one component is present.
**Action:** When an interface has both mobile and desktop variants of the same control in the DOM, ensure RTL tests handle multiple elements (e.g., using `getAllByRole(...)[0] as HTMLElement` and `.length > 0` assertions).
