## 2024-10-17 - Add memory limit to file uploads
**Vulnerability:** Unbounded file read in `POST /uploads` can cause excessive memory allocation.
**Learning:** Using `file.read()` without a byte limit on user uploads bypasses memory constraints before the configured size limit check occurs.
**Prevention:** Always pass a maximum byte limit (e.g., `file.read(max_bytes + 1)`) when reading uploaded files into memory.
