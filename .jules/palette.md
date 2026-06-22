## 2024-04-18 - Added keyboard shortcuts to AI Chat textarea
**Learning:** In chat interfaces, users expect `Enter` to submit the message and `Shift+Enter` for new lines. Providing a visual `<kbd>` hint improves discoverability. Disabling the textarea during streaming prevents prompt mangling.
**Action:** Always implement `Enter` to submit for chat inputs, include a visual hint, and ensure the input is disabled during asynchronous operations like streaming.
