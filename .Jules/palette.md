## 2026-03-05 - Password Visibility Toggle in Generic Component
**Learning:** Adding complex state logic (like password visibility) directly to low-level primitive UI components (like Input) ensures that every form in the application automatically benefits from the UX improvement without developers needing to remember to compose wrappers or implement state per-form.
**Action:** When identifying common UI states (visibility, clearability, loading), attempt to implement them inside the design system primitive instead of the specific feature view.
