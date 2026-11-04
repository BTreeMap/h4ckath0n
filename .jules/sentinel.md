## 2026-09-28 - [Sanitize file download filename]
**Vulnerability:** Path traversal via malicious uploaded filenames returned in Content-Disposition.
**Learning:** Even if a file is safely stored with an opaque key, if its original user-supplied filename is used directly in FileResponse or Content-Disposition, it can cause client-side path traversal or arbitrary file writes during download.
**Prevention:** Always sanitize user-supplied filenames on download by applying `os.path.basename` (after replacing Windows path separators) to prevent path traversal on the client machine.
