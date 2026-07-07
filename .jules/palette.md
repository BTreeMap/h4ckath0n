## 2026-07-07 - Added ARIA labels to mobile toggle buttons
**Learning:** When adding identical aria-labels to elements that appear multiple times in the DOM (like desktop vs mobile variants), React Testing Library's getByRole will fail with a 'multiple elements found' error. You must switch to getAllByRole()[0]! to handle the duplicate elements properly.
**Action:** Always check if a UI component exists in multiple responsive versions before adding aria attributes, and update RTL tests to use getAllByRole when necessary.
