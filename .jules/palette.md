## 2024-05-18 - Mobile/Desktop Component Testing
**Learning:** Adding accessible attributes (`aria-label`) to duplicate UI elements (mobile vs. desktop variants) in the React frontend causes React Testing Library queries using `getByRole` to fail with multiple elements found.
**Action:** When adding labels to duplicate elements, update corresponding testing queries from `getByRole` to `getAllByRole(...)[0]!` to prevent test failures and satisfy TypeScript strict mode constraints during Vite builds.
