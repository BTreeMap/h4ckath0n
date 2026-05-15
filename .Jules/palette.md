## 2024-03-14 - Responsive duplicate components and a11y attributes
**Learning:** When adding accessibility attributes like `aria-label` to components with responsive duplicates (e.g., desktop and mobile variants of a toggle button that are both rendered but hidden via CSS media queries), it can cause unit tests using `getByRole` to fail with "Found multiple elements".
**Action:** Always verify if a component has responsive duplicates before adding accessibility attributes, and update corresponding unit tests to use `getAllByRole('...')[0]!` instead of `getByRole` to prevent build failures.
