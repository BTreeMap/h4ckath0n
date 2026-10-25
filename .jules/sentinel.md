## 2023-10-25 - Limit memory allocation when reading uploaded files
**Vulnerability:** Missing input length limits on file reads.
**Learning:** FastAPI `UploadFile` reads the entire file content into memory regardless of size when called without arguments, ignoring configured limits.
**Prevention:** Always pass a maximum byte limit (e.g., `file.read(max_bytes + 1)`) when explicitly reading uploaded files.
