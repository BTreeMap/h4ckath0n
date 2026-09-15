## 2024-07-19 - Prevent OOM DoS from Unbounded File Reads
**Vulnerability:** FastAPI `UploadFile.read()` called without arguments reads the entire file into memory at once, which can cause OOM DoS.
**Learning:** Checking length after an unbounded read is too late as the memory is already allocated.
**Prevention:** Use `file.size` where available to reject early, and pass a bound to `file.read()` (e.g., `await file.read(max_bytes + 1)`).
