## 2024-05-24 - [OOM DoS via File Uploads]
**Vulnerability:** FastAPIs `await file.read()` is called without a byte limit before the size check, allowing an attacker to consume arbitrary amounts of memory.
**Learning:** Checking the length of the data *after* reading the entire file into memory defeats the purpose of the limit for security against DoS.
**Prevention:** Always pass a byte limit to `file.read(max_bytes + 1)` so the underlying stream stops buffering once the limit is exceeded, preventing OOM DoS.
