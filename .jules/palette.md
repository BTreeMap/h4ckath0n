## 2024-10-31 - [Visual Required Indicators]
 **Learning:** React Testing Library's exact string matches for getByLabelText fail when appending visual indicators (like an asterisk) inside a Label element, even if marked aria-hidden="true".
 **Action:** Update affected tests to use regex matches (e.g., getByLabelText(/Label/i)) when adding visual required indicators to reusable form components.
