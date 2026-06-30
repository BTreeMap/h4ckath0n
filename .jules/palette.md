## 2024-06-30 - Accessible Duplicate Elements
**Learning:** When adding aria-labels to duplicate UI elements (like mobile vs desktop theme toggles), React Testing Library queries using getByRole will fail due to multiple elements found, even if one is visually hidden by responsive classes (like md:hidden).
**Action:** Update RTL queries from getByRole to getAllByRole(...)[0]! to handle duplicated accessible elements while satisfying strict TypeScript constraints.
