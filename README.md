# h4ckrth0n

Ship hackathon products fast, with secure-by-default auth, RBAC, Postgres readiness, and built-in LLM tooling.

**h4ckrth0n** is an opinionated Python library that makes it hard to accidentally ship insecure glue code during a hackathon.

## What you get by default

- **API**: FastAPI app bootstrap with OpenAPI docs
- **Auth**: registration, login, JWT access tokens, refresh tokens (revocable), password reset (single-use, time-limited)
- **AuthZ**: built-in RBAC with `user` and `admin` roles, plus scoped permissions via JWT claims
- **Database**: SQLAlchemy 2.x + Alembic, works with SQLite (zero-config) and Postgres (driver included)
- **LLM**: built-in LLM client wrapper (OpenAI SDK) with safe defaults and redaction hooks
- **Observability**: opt-in LangSmith / OpenTelemetry tracing with trace ID propagation
- **Config**: environment-driven settings via pydantic-settings

Redis-based queues/caching are available as an optional extra.

## Installation

### Recommended (uv)

```bash
uv add h4ckrth0n
```

Optional Redis support:

```bash
uv add "h4ckrth0n[redis]"
```

### pip

```bash
pip install h4ckrth0n
```

## Quickstart

```python
from h4ckrth0n import create_app

app = create_app()
```

Run:

```bash
uv run uvicorn your_module:app --reload
```

Open docs at `/docs` (Swagger UI).

## Secure-by-default endpoint protection

Protect an endpoint (requires a logged-in user):

```python
from h4ckrth0n import create_app
from h4ckrth0n.auth import require_user

app = create_app()

@app.get("/me")
def me(user=require_user()):
    return {"id": user.id, "email": user.email, "role": user.role}
```

Admin-only endpoint:

```python
from h4ckrth0n.auth import require_admin

@app.get("/admin/dashboard")
def admin_dashboard(user=require_admin()):
    return {"ok": True}
```

Scoped privileges (JWT claim `scopes`):

```python
from h4ckrth0n.auth import require_scopes

@app.post("/billing/refund")
def refund(user=require_scopes("billing:refund")):
    return {"status": "queued"}
```

## Auth routes

h4ckrth0n mounts auth routes under `/auth` by default:

- `POST /auth/register` – create account (returns access + refresh tokens)
- `POST /auth/login` – authenticate (returns access + refresh tokens)
- `POST /auth/refresh` – rotate refresh token, get new access token
- `POST /auth/logout` – revoke refresh token
- `POST /auth/password-reset/request` – request a password reset
- `POST /auth/password-reset/confirm` – confirm reset with token + new password

## Database

Zero-config default: SQLite is used if no database URL is provided.

To use Postgres, set:

```
H4CKRTH0N_DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname
```

The `psycopg[binary]` driver is included by default – no extra install needed.

## LLM

h4ckrth0n includes LLM tooling by default. Set `OPENAI_API_KEY` and use:

```python
from h4ckrth0n.llm import llm

client = llm()
resp = client.chat(
    system="You are a helpful assistant.",
    user="Summarize this in one sentence: ...",
)
print(resp.text)
```

Fails gracefully with a clear error message when `OPENAI_API_KEY` is not set.

## Configuration

Everything is environment-driven (prefix `H4CKRTH0N_`):

| Variable | Default | Description |
|---|---|---|
| `H4CKRTH0N_ENV` | `development` | `development` or `production` |
| `H4CKRTH0N_DATABASE_URL` | `sqlite:///./h4ckrth0n.db` | Database connection string |
| `H4CKRTH0N_AUTH_SIGNING_KEY` | *(ephemeral in dev)* | JWT signing key (**required in production**) |
| `H4CKRTH0N_BOOTSTRAP_ADMIN_EMAILS` | `[]` | JSON list of emails that get admin role on registration |
| `H4CKRTH0N_FIRST_USER_IS_ADMIN` | `false` | First registered user becomes admin (dev convenience) |
| `OPENAI_API_KEY` | — | OpenAI API key for the LLM module |

In development mode, missing signing keys generate ephemeral secrets with a warning.
In production mode, missing critical secrets cause a hard error.

## Observability (opt-in)

Enable end-to-end tracing across FastAPI requests, LangGraph nodes, tool calls, and LLM calls.

### Enable LangSmith tracing

```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=your-project-name
```

### Trace IDs

When observability is enabled, h4ckrth0n attaches `X-Trace-Id` to all responses:

```python
from h4ckrth0n import create_app
from h4ckrth0n.obs import init_observability

app = create_app()
init_observability(app)
```

## Development

```bash
git clone https://github.com/BTreeMap/h4ckrth0n.git
cd h4ckrth0n
uv sync
uv run pytest
```

Quality gates:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
```

Build:

```bash
uv build
```

## License

MIT. See `LICENSE`.

