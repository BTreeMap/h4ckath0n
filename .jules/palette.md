## 2024-04-26 - Keyboard accessibility for hidden interactive elements
**Learning:** Elements hidden via `opacity-0 group-hover:opacity-100` remain invisible when focused via keyboard, and `sr-only` radio inputs nested inside interactive labels do not show focus states unless the label is explicitly styled.
**Action:** Use `focus-visible:opacity-100` on hover-revealed elements, and `has-[:focus-visible]:ring-2` on parent labels wrapping visually hidden inputs.
