## 2025-04-14 - Chat Textarea Enhancements
**Learning:** Users naturally expect chat textareas to submit via the Enter key. Adding an absolute-positioned hint requires extra padding on the textarea to avoid text overlap, and the textarea should be disabled during streaming to prevent prompt mangling.
**Action:** When implementing chat interfaces, always add `onKeyDown` for Enter-to-submit, disable the input during async operations, and ensure adequate padding (e.g., `pb-8`) for hint elements.
