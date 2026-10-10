<<<<<<< SEARCH
## Configuration

All settings use the `H4CKATH0N_` prefix unless noted.

| Variable | Default | Description |
|---|---|---|
| `H4CKATH0N_ENV` | `development` | `development` or `production` |
| `H4CKATH0N_DATABASE_URL` | `sqlite:///./h4ckath0n.db` | SQLAlchemy connection string |
| `H4CKATH0N_AUTO_UPGRADE` | `false` | Auto-run packaged DB migrations to head on startup |
| `H4CKATH0N_RP_ID` | `localhost` in development | WebAuthn relying party ID, required in production |
| `H4CKATH0N_ORIGIN` | `http://localhost:8000` in development | WebAuthn origin, required in production |
| `H4CKATH0N_WEBAUTHN_TTL_SECONDS` | `300` | WebAuthn challenge TTL in seconds |
| `H4CKATH0N_USER_VERIFICATION` | `preferred` | WebAuthn user verification requirement |
| `H4CKATH0N_ATTESTATION` | `none` | WebAuthn attestation preference |
| `H4CKATH0N_PASSWORD_AUTH_ENABLED` | `false` | Enable password routes when the extra is installed |
| `H4CKATH0N_PASSWORD_RESET_EXPIRE_MINUTES` | `30` | Password reset token expiry in minutes |
| `H4CKATH0N_BOOTSTRAP_ADMIN_EMAILS` | `[]` | JSON list of emails that become admin on password signup |
| `H4CKATH0N_FIRST_USER_IS_ADMIN` | `false` | First password signup becomes admin |
| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |
| `H4CKATH0N_OPENAI_API_KEY` | empty | Alternate OpenAI API key for the LLM wrapper |
| `H4CKATH0N_REDIS_URL` | empty | Redis connection string |
| `H4CKATH0N_JOBS_INLINE_IN_DEV` | `true` | Run background jobs inline in development mode |
| `H4CKATH0N_JOBS_DEFAULT_QUEUE` | `default` | Default Redis queue for background jobs |
| `H4CKATH0N_STORAGE_BACKEND` | `local` | Storage backend |
| `H4CKATH0N_STORAGE_DIR` | `./.h4ckath0n_storage` | Local directory for uploaded files |
| `H4CKATH0N_MAX_UPLOAD_BYTES` | `52428800` | Maximum upload size in bytes (50 MiB) |
| `H4CKATH0N_APP_BASE_URL` | `http://localhost:5173` | Application base URL for email links |
| `H4CKATH0N_EMAIL_BACKEND` | `file` | Email backend: `file` or `smtp` |
| `H4CKATH0N_EMAIL_FROM` | `noreply@localhost` | Sender address for outgoing emails |
| `H4CKATH0N_EMAIL_OUTBOX_DIR` | `./.h4ckath0n_email_outbox` | File-backend email output directory |
| `H4CKATH0N_SMTP_HOST` | empty | SMTP server host |
| `H4CKATH0N_SMTP_PORT` | `587` | SMTP server port |
| `H4CKATH0N_SMTP_USERNAME` | empty | SMTP authentication username |
| `H4CKATH0N_SMTP_PASSWORD` | empty | SMTP authentication password |
| `H4CKATH0N_SMTP_STARTTLS` | `true` | Enable SMTP STARTTLS |
| `H4CKATH0N_SMTP_SSL` | `false` | Enable SMTP-over-SSL |
| `H4CKATH0N_DEMO_MODE` | `false` | Enable demo mode |
=======
## Configuration

All settings use the `H4CKATH0N_` prefix unless noted.

<!-- START ENV DOCS -->
| Variable | Default | Description |
|---|---|---|
<!-- END ENV DOCS -->
>>>>>>> REPLACE
