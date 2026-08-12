## 2025-03-08 - FastAPI CORSMiddleware Crash on Startup

**Vulnerability:** Adding FastAPI `CORSMiddleware` with `allow_origins=["*"]` alongside `allow_credentials=True`.
**Learning:** This configuration violates the CORS specification. In modern Starlette (used by FastAPI), this causes the application to crash synchronously upon startup with an exception, preventing the API from booting entirely.
**Prevention:** Always configure `CORSMiddleware` with explicitly allowed origins (e.g., `["http://localhost:5173"]`) when `allow_credentials=True` is required.
