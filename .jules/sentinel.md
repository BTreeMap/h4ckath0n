## 2024-10-18 - Unbounded File Upload Read
**Vulnerability:** Unbounded memory allocation when calling `await file.read()` during file uploads.
**Learning:** Calling `await file.read()` without limits will load the entire file into memory before size checks, which can lead to Out-Of-Memory (OOM) Denial of Service (DoS) attacks.
**Prevention:** Always pass a maximum byte limit, such as `file.read(max_bytes + 1)`, when explicitly reading uploaded files in FastAPI to cap memory usage.
