## 2024-05-23 - Add keyboard interactions to AI chat
 **Learning:** AI chat textareas must provide standard messaging affordances (Enter to send, Shift+Enter for newlines) while matching the exact disabled state conditions of the submit button to prevent users from mangling their prompt during streaming.
 **Action:** Always pair `onKeyDown` shortcut handlers with strict `disabled` states and clear visual hints (`<kbd>`) in streaming/chat interfaces.
