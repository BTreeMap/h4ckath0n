## 2024-06-11 - Adding aria labels to buttons
**Learning:** For components that duplicate elements for different viewports (like a mobile and desktop theme toggle button), you can't use `getByRole` directly in tests since it will find multiple elements. Instead, you need to use `getAllByRole` and select the correct index, e.g. `getAllByRole("button", { name: "Theme: light" })[0]`.

**Action:** When updating tests that might have duplicated responsive elements, prefer using `getAllByRole("...")[0]` instead of `getByRole("...")`. Always make sure to include a non-null assertion like `[0]!` in TypeScript environments to avoid build errors.
