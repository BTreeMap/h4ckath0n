## 2026-06-07 - Adding ARIA attributes can break test queries
**Learning:** When adding `aria-label` to identical components hidden contextually (e.g., desktop/mobile toggles), `getByRole` tests will fail by finding multiple matches.
**Action:** Update affected tests to expect multiple matches and use `getAllByRole()[0]`, and explicitly assert definition using `expect(element).toBeDefined()` before firing events to satisfy strict TypeScript/Vite environments.
