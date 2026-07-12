## 2026-07-12 - Add ARIA labels to mobile layout buttons
**Learning:** When duplicate UI variants exist for responsive layouts, accessibility attributes like aria-label should remain identical. The corresponding tests using screen.getByRole often need to be updated to screen.getAllByRole()[0] to avoid 'multiple elements found' errors in vitest.
**Action:** Remember to explicitly update React Testing Library test queries to support multiple duplicate ARIA labels when introducing mobile-responsive accessibility improvements.
