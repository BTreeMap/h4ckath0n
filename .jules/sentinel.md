## 2024-10-24 - Unbounded File Read
**Vulnerability:** Unbounded file read in upload router
**Learning:** `await file.read()` loads the entire file into memory before size checks are applied.
**Prevention:** Always pass `max_bytes + 1` to `file.read()` to limit memory usage.
