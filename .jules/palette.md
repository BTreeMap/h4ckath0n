## 2026-05-07 - Added focus-visible styles with matching border-radius to PasswordField toggle
**Learning:** When adding focus rings to absolute positioned interactive elements overlaying input fields, explicitly match the parent's border radius (e.g., `rounded-r-xl`) so the focus ring doesn't overflow visually.
**Action:** Use matching `rounded-*` utilities on absolutely positioned elements inside rounded containers.
