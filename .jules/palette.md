## 2026-07-06 - Added accessible attributes to duplicate UI elements
**Learning:** When adding accessible attributes (like aria-label) to duplicate UI elements (e.g. mobile vs. desktop variants) in the React frontend, update corresponding React Testing Library queries from getByRole to getAllByRole(...)[0]! to prevent 'multiple elements found' test failures and satisfy TypeScript strict mode constraints during Vite builds.
**Action:** Remember this pattern when writing or updating tests for responsive UI components.
