## 2024-04-17 - [Add Enter-to-submit to AI Chat]
**Learning:** Textarea inputs for AI chat components without Enter-to-submit interactions are unintuitive. Users naturally press Enter to send chat messages. Adding this along with a visual hint (`<kbd>Enter</kbd>`) improves both intuitiveness and accessibility.
**Action:** Always consider Enter-to-submit patterns for single-message oriented textarea inputs, ensuring to disable the input during async processing and preserving `Shift+Enter` for multiline text.
