
## 2026-07-09 - Handling accessibility in duplicate UI variants
**Learning:** When adding accessible attributes (like aria-label) to duplicate UI elements (e.g. mobile vs. desktop variants) in the React frontend, you must update corresponding React Testing Library queries from getByRole to getAllByRole(...)[0]! to prevent 'multiple elements found' test failures and satisfy TypeScript strict mode constraints.
**Action:** Always check for existing tests that might break when adding aria attributes to duplicate elements, and use getAllByRole for test stability.
