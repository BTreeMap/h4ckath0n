
## 2026-07-08 - Duplicate UI Element Testing
**Learning:** When fixing accessibility by adding ARIA labels to duplicate UI elements (like desktop/mobile menus), React Testing Library queries must be updated from getByRole to getAllByRole(...)[0]! to prevent 'multiple elements found' test failures.
**Action:** Anticipate test breakage when fixing a11y on responsive components with duplicate mobile/desktop variants and proactively update test queries.
