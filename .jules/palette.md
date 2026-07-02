## 2024-04-08 - Added Enter-to-submit to AI chat input
**Learning:** Adding keyboard shortcuts (like Enter to submit) significantly improves chat interface usability, but the input must be explicitly disabled during async responses to prevent prompt mangling. Additionally, absolutely positioned hints need corresponding padding on the textarea to prevent text overlap.
**Action:** Always implement Enter-to-submit with a `disabled` state and visible hint for chat-like textareas.
