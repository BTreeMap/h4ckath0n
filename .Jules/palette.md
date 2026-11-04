## 2025-02-15 - Prefer isLoading prop over manual text swapping for buttons
**Learning:** Swapping button text (e.g. "Upload" -> "Uploading...") during loading states causes the button to resize unexpectedly, creating a jarring UX.
**Action:** Use the `Button` component's built-in `isLoading` prop which correctly handles disabled state and displays a spinner while maintaining button width for a smoother interaction.
