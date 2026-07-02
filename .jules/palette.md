## 2026-04-19 - [Enter-to-submit Interaction]
 **Learning:** In chat interfaces, users expect Enter-to-submit functionality. Furthermore, the textarea must be disabled during streaming to avoid mangled prompts, and adequate bottom padding (pb-8) must be added when placing absolute-positioned hint elements to avoid text overlap.
 **Action:** Implement Enter-to-submit keyboard handling on prompt textareas, ensuring the input is not empty before submitting. Use disabled attributes during async tasks, and allocate layout space (like pb-8) for absolute-positioned elements.
