## 2024-04-12 - Enter-to-submit and Async Textarea States
**Learning:** When implementing Enter-to-submit in chat textareas, the textarea must be disabled during async operations (like streaming) to prevent users from mangling the active stream. Also, adding absolute-positioned `<kbd>` hints requires adequate bottom padding (`pb-8`) on the textarea to prevent text from overlapping the hint.
**Action:** Always apply the `disabled` attribute directly to the textarea and ensure `pb-8` is added when placing bottom-aligned absolute elements inside textarea containers.
