## 2024-05-24 - Chat Interface Keyboard UX
**Learning:** During AI streaming operations, keeping the prompt textarea active can lead to prompt mangling if the user continues typing or submits again before the stream finishes. Providing keyboard shortcuts (Enter to submit) requires explicitly disabling the input and showing visual `<kbd>` hints to establish a natural interaction model.
**Action:** Always disable textareas during async stream processing and add `pb-8` padding when floating a `<kbd>` hint to prevent text overlap.
