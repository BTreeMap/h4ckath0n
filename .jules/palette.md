## 2024-07-02 - Mobile Icon Accessibility
**Learning:** When adding `aria-label`s to duplicated responsive UI elements (like mobile/desktop variants), React Testing Library tests that previously relied on `getByRole` will fail due to finding multiple elements.
**Action:** Update tests to use `getAllByRole(...)[0]!` to select the first matching instance and avoid "multiple elements found" errors while ensuring strict TypeScript compliance.
