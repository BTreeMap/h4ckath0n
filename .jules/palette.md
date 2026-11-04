## 2024-10-07 - Test Resilience with Visual Labels
**Learning:** When modifying React component labels with visual additions (like required asterisks), standard string matching in React Testing Library (e.g. `getByLabelText('Email')`) will fail because the text content includes the new elements.
**Action:** Update associated React Testing Library queries to use regex matching (e.g., `getByLabelText(/Email/)`) instead of exact string matches to maintain test resilience against visual label enhancements.
