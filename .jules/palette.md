## 2024-04-02 - Visual keyboard shortcut hints
**Learning:** Users often don't realize they can use "Enter" to submit textareas or custom inputs. Adding a small `<kbd>` hint near the input/button significantly improves discoverability of the shortcut and provides a more pro-user feel.
**Action:** Whenever adding custom `onKeyDown` handlers for "Enter" submission, pair it with a visual `<kbd>` hint.
