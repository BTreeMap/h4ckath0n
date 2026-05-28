## 2024-05-28 - Missing responsive ARIA labels and skip link
**Learning:** Responsive icon buttons (like mobile menus and theme switchers) need explicit `aria-label`s and tests using `getByRole` must handle duplicate hidden elements. Also, missing skip-to-content links break keyboard navigation.
**Action:** Always verify mobile views for screen reader accessibility, provide explicit `aria-label`s for icon buttons, ensure test resilience against responsive hidden elements, and include skip links.
