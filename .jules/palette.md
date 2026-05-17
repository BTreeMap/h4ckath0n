## 2024-05-17 - [Skip-to-content and multiple elements testing]
 **Learning:** When adding ARIA labels to responsive UI elements that are duplicated (like the theme toggle button for desktop vs mobile), existing tests using `getByRole` will break because it now matches multiple elements instead of one.
 **Action:** Update test logic to account for multiple matching elements using `getAllByRole(...)[0]` or similar query combinations when duplicating attributes for responsive design.
