## 2026-04-30 - Interactive elements hidden via group-hover require focus-visible styles
**Learning:** Interactive elements hidden via `opacity-0 group-hover:opacity-100` are inaccessible to keyboard users because they remain transparent when receiving focus.
**Action:** When hiding interactive elements visually using hover opacity, always append `focus-visible:opacity-100` so they become visible upon receiving keyboard focus.
