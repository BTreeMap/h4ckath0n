## 2024-05-23 - Prevent DoS via uncontrolled file upload reads
**Vulnerability:** The `/uploads` endpoint called `await file.read()` which loaded the entire upload into RAM before checking the length against `settings.max_upload_bytes`, allowing an attacker to cause an Out-Of-Memory (OOM) crash by uploading a massive file.
**Learning:** Even if a framework handles large uploads gracefully via SpooledTemporaryFile to disk, explicitly calling `read()` without limits eagerly loads the file into memory.
**Prevention:** Always pass a maximum byte limit to `.read(max_bytes)` corresponding to the application's configuration to prevent uncontrolled memory allocation.
