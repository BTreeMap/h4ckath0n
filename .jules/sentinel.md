## 2024-10-19 - DoS Risk in Upload Router via Unbounded Read
**Vulnerability:** The `/uploads` endpoint was reading user-supplied files entirely into memory using `await file.read()` before checking the length against `settings.max_upload_bytes`.
**Learning:** This approach opens the app to an Out-Of-Memory (OOM) Denial of Service (DoS) attack. A malicious user could stream a massive file (e.g., several gigabytes) which would be fully buffered in memory before the length check is evaluated, crashing the worker.
**Prevention:** Always pass a maximum byte limit to `.read()` (e.g., `file.read(max_bytes + 1)`) when explicitly loading files into memory in FastAPI, so the operation terminates early if the stream exceeds the limit.
