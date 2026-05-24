## 2024-05-24 - Accessibility on Responsive Layout elements
**Learning:** Added skip-to-main-content hidden element and updated ARIA labels. I also noticed tests using `getByRole` need to handle multiple items like `getAllByRole(...)[0]` when components have duplicated elements hidden by CSS for responsive modes.
**Action:** When making accessible changes that impact responsive layout menus or toggle elements which exist in desktop vs. mobile, update associated vitest RTL checks to target explicitly the first element using `getAllByRole(...)[0]`.
