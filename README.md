# h4ckrth0n

Ship hackathon products fast, with secure-by-default auth, RBAC, Postgres readiness, and built-in LLM tooling.

**h4ckrth0n** is an opinionated Python library that makes it hard to accidentally ship insecure glue code during a hackathon.

## What you get by default

- **API**: FastAPI app bootstrap with docs
- **Auth**: registration, login, JWT access tokens, refresh tokens (revocable), password reset
- **AuthZ**: built-in RBAC with `user` and `admin`, plus scoped permissions via JWT claims
- **Database**: SQLAlchemy + Alembic, works with SQLite (zero-config) and Postgres (driver included)
- **LLM**: built-in LLM client wrapper (OpenAI SDK under the hood) with safe defaults and redaction hooks
- **Config**: environment-driven settings

Redis-based queues/caching are optional.

## Installation

### Recommended (uv)

```bash
uv add h4ckrth0n
````

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

Open docs:

* Swagger UI: `/docs`

## Secure-by-default endpoint protection

Protect an endpoint (requires a logged-in user):

```python
from h4ckrth0n import create_app
from h4ckrth0n.auth import require_user

app = create_app()

@app.get("/me")
def me(user = require_user()):
    return {"id": user.id, "email": user.email, "role": user.role}
```

Admin-only endpoint:

```python
from h4ckrth0n.auth import require_admin

@app.get("/admin/dashboard")
def admin_dashboard(user = require_admin()):
    return {"ok": True}
```

Scoped privileges (JWT claim `scopes`):

```python
from h4ckrth0n.auth import require_scopes

@app.post("/billing/refund")
def refund(user = require_scopes("billing:refund")):
    return {"status": "queued"}
```

## Auth routes

h4ckrth0n mounts auth routes under `/auth` by default:

* `POST /auth/register`
* `POST /auth/login`
* `POST /auth/refresh`
* `POST /auth/logout`
* `POST /auth/password-reset/request`
* `POST /auth/password-reset/confirm`

## Database

Zero-config default: SQLite is used if no database URL is provided.

To use Postgres, set:

* `H4CKRTH0N_DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname`

Migrations are powered by Alembic.

## LLM

h4ckrth0n includes LLM tooling by default. It uses the official OpenAI Python SDK and reads credentials from environment variables. ([OpenAI Platform][3])

Example:

```python
from h4ckrth0n.llm import llm

client = llm()

resp = client.chat(
    system="You are a helpful assistant.",
    user="Summarize this in one sentence: ...",
)
print(resp.text)
```

## Configuration

Everything is environment-driven.

Minimum recommended settings for real deployments:

* `H4CKRTH0N_ENV=production`
* `H4CKRTH0N_AUTH_SIGNING_KEY=...`
* `H4CKRTH0N_DATABASE_URL=...`

In development, h4ckrth0n can generate ephemeral secrets to reduce setup friction, but production mode should fail closed if secrets are missing.

## Development

```bash
git clone https://github.com/username/h4ckrth0n.git
cd h4ckrth0n
uv sync
uv run pytest
```

Quality gates:

```bash
uv run ruff format .
uv run ruff check .
uv run mypy src
uv run pytest
```

## License

MIT. See `LICENSE`.

