## 2024-05-24 - [Bind loading state to aria-busy in interactive elements]
 **Learning:** React components (especially buttons and spinners) require explicit `aria-busy` attributes bound to their loading states and `aria-hidden="true"` on internal decorative spinner icons to ensure proper screen reader announcement of the transient UI state.
 **Action:** When utilizing or implementing interactive elements that reflect async operations, consistently apply `aria-busy={isLoading}` on the host element and `aria-hidden="true"` to decorative loading indicators.
