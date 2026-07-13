## 2024-07-13 - [Mobile ARIA Labels]
**Learning:** Added ARIA labels to mobile layout buttons but caused testing failures because `getByRole` conflicted with desktop buttons that share the identical accessible name.
**Action:** When adding accessibility attributes to responsive UI components that are duplicated for mobile/desktop, update test cases to use `.getAllByRole(...)[0]` to handle the duplicate rendering safely.
