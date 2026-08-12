## 2024-05-15 - AI Prompt Enter-to-Submit
**Learning:** Users instinctively expect to press Enter to submit chat/prompt inputs. When adding this behavior, applying `disabled` to the textarea during async operations prevents prompt mangling, and a `<kbd>` hint with bottom padding clarifies the interaction model without overlapping text.
**Action:** Always implement Enter-to-submit with a visible hint and disabled state for async operations in chat-like textareas.
