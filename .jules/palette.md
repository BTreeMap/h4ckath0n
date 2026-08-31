## 2026-04-05 - AI Chat Textarea Keyboard Interaction
**Learning:** Implementing Enter-to-submit in textareas (especially for AI prompts) requires explicitly disabling the textarea during async operations (streaming) to prevent user input from mangling the prompt while it's being sent. Visual <kbd> hints also need dedicated spacing (e.g., pb-8) to prevent overlap with the textarea text.
**Action:** Apply disabled states directly to textareas during async submissions and ensure absolute positioned hints have corresponding padding in the parent element.
