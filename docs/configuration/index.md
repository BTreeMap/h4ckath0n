# Configuration

h4ckath0n is configured entirely through environment variables using Pydantic Settings.

## Environment Variables

<!-- ENV_VARS_START -->
| Environment Variable | Type | Default |
| --- | --- | --- |
| `H4CKATH0N_ENV` | string | `development` |
| `H4CKATH0N_DATABASE_URL` | string | `sqlite:///./h4ckath0n.db` |
| `H4CKATH0N_AUTO_UPGRADE` | boolean | `False` |
| `H4CKATH0N_RP_ID` | string | `''` |
| `H4CKATH0N_ORIGIN` | string | `''` |
| `H4CKATH0N_WEBAUTHN_TTL_SECONDS` | integer | `300` |
| `H4CKATH0N_USER_VERIFICATION` | string | `preferred` |
| `H4CKATH0N_ATTESTATION` | string | `none` |
| `H4CKATH0N_PASSWORD_AUTH_ENABLED` | boolean | `False` |
| `H4CKATH0N_PASSWORD_RESET_EXPIRE_MINUTES` | integer | `30` |
| `H4CKATH0N_BOOTSTRAP_ADMIN_EMAILS` | string | `[]` |
| `H4CKATH0N_FIRST_USER_IS_ADMIN` | boolean | `False` |
| `H4CKATH0N_OPENAI_API_KEY` | string | `''` |
| `H4CKATH0N_REDIS_URL` | string | `''` |
| `H4CKATH0N_JOBS_INLINE_IN_DEV` | boolean | `True` |
| `H4CKATH0N_JOBS_DEFAULT_QUEUE` | string | `default` |
| `H4CKATH0N_STORAGE_BACKEND` | string | `local` |
| `H4CKATH0N_STORAGE_DIR` | string | `./.h4ckath0n_storage` |
| `H4CKATH0N_MAX_UPLOAD_BYTES` | integer | `52428800` |
| `H4CKATH0N_APP_BASE_URL` | string | `http://localhost:5173` |
| `H4CKATH0N_EMAIL_BACKEND` | string | `file` |
| `H4CKATH0N_EMAIL_FROM` | string | `noreply@localhost` |
| `H4CKATH0N_EMAIL_OUTBOX_DIR` | string | `./.h4ckath0n_email_outbox` |
| `H4CKATH0N_SMTP_HOST` | string | `''` |
| `H4CKATH0N_SMTP_PORT` | integer | `587` |
| `H4CKATH0N_SMTP_USERNAME` | string | `''` |
| `H4CKATH0N_SMTP_PASSWORD` | string | `''` |
| `H4CKATH0N_SMTP_STARTTLS` | boolean | `True` |
| `H4CKATH0N_SMTP_SSL` | boolean | `False` |
| `H4CKATH0N_DEMO_MODE` | boolean | `False` |
<!-- ENV_VARS_END -->
