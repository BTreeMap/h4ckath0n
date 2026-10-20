## 2025-02-14 - Fix Out-Of-Memory DoS in File Uploads
**Vulnerability:** The `upload_file` endpoint read the entire uploaded file into memory (`await file.read()`) before evaluating if its length exceeded the `max_upload_bytes` setting, creating an Out-Of-Memory (OOM) Denial of Service risk.
**Learning:** In FastAPI, `UploadFile.read()` loads everything into memory if no maximum bytes parameter is passed. Application-level length checks performed *after* an unconstrained read offer no protection against resource exhaustion.
**Prevention:** Always pass an explicit upper bound to `file.read()` (e.g., `max_upload_bytes + 1`) when buffering user uploads in memory to enforce size limits safely.
