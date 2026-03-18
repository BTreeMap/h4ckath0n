## 2025-03-18 - Accessibility for Responsive Duplicates
**Learning:** Adding `aria-label` to duplicate responsive elements (like desktop and mobile theme toggles) causes tests using `getByRole` to fail.
**Action:** When adding accessibility features to responsive duplicates, update tests to use `getAllByRole(...)[0]!` to prevent "multiple elements found" errors while satisfying strict TypeScript checks.
