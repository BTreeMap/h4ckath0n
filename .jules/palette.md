## 2024-04-15 - Enter to Submit in AI prompt textareas
 **Learning:** In chat interfaces, like the AI stream panel in Dashboard.tsx, users expect to be able to submit their prompt by pressing 'Enter' while inside the textarea, but they also might want to type multiple lines (Shift+Enter). We need to handle this keydown interaction, check if the prompt is not empty, and disable the textarea during stream parsing.
 **Action:** Add a custom onKeyDown handler to AI prompt textareas that triggers submission on Enter (without Shift) and disables the input while streaming to prevent prompt mangling.
