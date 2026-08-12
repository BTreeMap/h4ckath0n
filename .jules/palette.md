## 2024-10-24 - [Add aria-busy to loading Button]
**Learning:** In React UI components with loading states, always bind the loading prop (e.g., isLoading) to the aria-busy attribute on the interactive element and apply aria-hidden="true" to any inner decorative spinner icons. This ensures screen readers properly announce the loading context.
**Action:** Consistently apply this pattern when adding or modifying loading states across interactive components.
