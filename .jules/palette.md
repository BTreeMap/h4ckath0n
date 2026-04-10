
## 2024-05-24 - AI Chat Input Interaction
**Learning:** AI chat textareas without Enter-to-submit feel broken to users used to standard messaging apps. Failing to disable the input during streaming allows accidental prompt mangling. Absolute-positioned hint overlays need matching bottom padding on the textarea (pb-8) to prevent text overlap.
**Action:** Always implement Enter-to-submit, disable the textarea during active streaming, and use pb-8 padding for <kbd> overlay hints in chat interfaces.
