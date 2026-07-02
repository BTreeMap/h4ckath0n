## 2025-02-12 - Keyboard Focus in Absolute Overlays
 **Learning:** When creating input appendages (like a password visibility toggle) absolutely positioned over the input field, the interactive element's focus ring must explicitly match the border radius of the underlying container's corner (e.g., `rounded-r-xl`) to prevent the focus ring from awkwardly overflowing into the input area.
 **Action:** For all future `absolute` interactive input overlays, ensure `focus-visible:ring-*` is accompanied by targeted border-radius utilities that mirror the parent container's shape.
