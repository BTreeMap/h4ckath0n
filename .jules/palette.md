## 2024-05-24 - Enhance AI Chat UX with Keyboard Shortcuts and ARIA attributes
**Learning:** Multiline textareas (like AI chat prompts) without explicit `aria-label`s and `aria-live` regions for streaming responses result in a poor screen reader experience. Furthermore, users expect `Cmd/Ctrl + Enter` to submit forms in chat interfaces.
**Action:** Always provide `aria-live="polite"` for dynamic streaming AI responses, attach `aria-label`s to unlabelled textareas, and implement `Cmd/Ctrl + Enter` shortcuts with visual `<kbd>` hints for chat inputs.
