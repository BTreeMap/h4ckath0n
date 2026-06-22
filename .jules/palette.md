## 2026-06-12 - Explicit ARIA Labels on Responsive Elements Fail Strict Testing Queries

**Learning:** When adding explicit `aria-label` attributes to responsive UI components (e.g., adding labels to icon-only mobile menu toggles or duplicate desktop/mobile theme toggles), `getByRole` assertions in tests will fail because they find multiple elements with identical accessible names (one visible, one visually hidden by CSS media queries).
**Action:** When adding responsive duplicate elements with identical accessible names for accessibility, explicitly update the associated testing queries from `getByRole` to `getAllByRole(...)[0]` (and `queryByRole` to `queryAllByRole(...).length === 0`) to handle the duplication gracefully in JSDOM, where CSS-based visibility is often ignored.

## 2026-06-12 - Skip to Main Content Pattern

**Learning:** A standard accessibility pattern for keyboard navigation requires a "Skip to main content" link that becomes visible on focus.
**Action:** When working on application layout structures, ensure there is an anchor link targeting `id="main-content"` at the very top of the DOM tree that becomes visually evident only on `focus-visible:` or `focus:` state.
