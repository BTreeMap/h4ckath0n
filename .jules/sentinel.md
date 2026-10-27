## 2026-10-27 - [Unbounded File Read in Uploads]
**Vulnerability:** Calling `await file.read()` on `UploadFile` without a maximum size limit.
**Learning:** `FastAPI`'s `UploadFile` stores uploads larger than a specific limit into disk. However, calling `await file.read()` without specifying a maximum size limit pulls the entire file into memory at once, creating an Out-Of-Memory (OOM) Denial of Service (DoS) vulnerability, even if checked against a maximum file size after the read.
**Prevention:** Always pass a byte limit to `file.read()` (e.g., `await file.read(max_bytes + 1)`) to avoid loading oversized files entirely into memory.
