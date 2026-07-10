## 2026-07-10 - Duplicated UI Accessibility Pattern
**Learning:** When duplicate interactive elements (like desktop/mobile toggles) share the same accessible name, it creates 'multiple elements found' errors in testing libraries.
**Action:** Use `getAllByRole(...)[0]` in tests to resolve the error while preserving the valid a11y label.
