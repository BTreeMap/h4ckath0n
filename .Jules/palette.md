## 2024-05-24 - Embed Universal Form Behaviors into Primitives
**Learning:** Adding universal form behaviors (like password visibility toggles) individually to every usage point often leads to inconsistent accessibility features (missing ARIA labels, inconsistent focus states) and redundant logic.
**Action:** Build these behaviors directly into design system primitive components (like `Input.tsx` for `type="password"`) rather than relying on developers to compose wrapper elements, ensuring automatic and consistent application of accessibility features.
