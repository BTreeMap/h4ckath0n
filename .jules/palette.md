## 2024-05-24 - Improve Button Loading State Accessibility
**Learning:** Screen readers only announce disabled processing buttons as "dimmed" if they lack an explicit `aria-busy="true"` state, which obscures the loading context.
**Action:** Always bind the `isLoading` state to `aria-busy` and apply `aria-hidden="true"` to decorative spinner icons in generic components.
