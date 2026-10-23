## 2025-02-14 - File Upload DoS via Memory Exhaustion
**Vulnerability:** The `upload_file` endpoint read the entire contents of a file into memory without bounds via `await file.read()`, leading to potential Out-Of-Memory (OOM) Denial of Service (DoS) attacks.
**Learning:** `fastapi.UploadFile.read()` loads everything into the active process memory if no size limit is provided, even if a size check follows later in the function.
**Prevention:** Pass `max_upload_bytes + 1` to `file.read()` to constrain memory usage while still enabling logic to catch oversized uploads securely.
