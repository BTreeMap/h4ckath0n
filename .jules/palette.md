## 2025-03-05 - Add aria-busy to loading buttons
**Learning:** Screen reader users need explicit loading states to understand when async actions (like auth) are processing, especially when icons change dynamically.
**Action:** Always bind the loading state (e.g., `isLoading`, `passkeyLoading`) to `aria-busy={...}` on buttons, and apply `aria-hidden="true"` to any inner decorative spinner icons (like `<Loader2 />`).
