## 2024-05-24 - Add focus styles to absolute interactive elements
**Learning:** When adding focus rings (`focus-visible:ring-*`) to absolutely positioned interactive elements overlaying input fields (e.g., password visibility toggles), the focus ring causes visual overflow if the container has rounded corners.
**Action:** Explicitly apply border-radius utilities (e.g., `rounded-r-xl`) that match the parent container's shape to prevent visual overflow and maintain design cohesiveness.
