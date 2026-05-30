## 2024-04-11 - Add Enter-to-submit keyboard interactions in textareas
**Learning:** When implementing Enter-to-submit keyboard interactions in textareas (like AI prompts), it's important to disable the textarea during async operations to prevent prompt mangling and provide adequate bottom padding (e.g., pb-8) for absolute-positioned <kbd> hints to prevent text overlap.
**Action:** Apply the `disabled` attribute directly to the textarea and use padding to make room for absolute-positioned visual hints.
