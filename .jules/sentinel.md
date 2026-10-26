## 2024-10-26 - Prevent uncontrolled memory allocation in FastAPI File Uploads
 **Vulnerability:** Uncontrolled memory allocation when explicitly reading uploaded files with `await file.read()`.
 **Learning:** Calling `await file.read()` without a byte limit reads the entire file into memory, which can lead to memory exhaustion.
 **Prevention:** Always pass a maximum byte limit (e.g., `file.read(max_bytes + 1)`) when explicitly reading uploaded files.