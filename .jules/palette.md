
## 2026-06-12 - Responsive Button ARIA Synchronization
**Learning:** When icon-only buttons (like a theme toggle) are duplicated for responsive layouts (e.g., hidden/shown via md:hidden or hidden md:flex), failing to add identical aria-label attributes to the mobile versions creates inconsistent accessibility experiences. Furthermore, adding these labels causes existing getByRole tests to fail due to multiple matches, requiring updates to handle arrays of elements.
**Action:** Always ensure responsive clones of icon-only controls receive identical ARIA states/labels as their desktop counterparts, and proactively update testing-library queries using getAllByRole and non-null assertions to handle the duplicated DOM nodes robustly.
