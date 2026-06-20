# Releases and dependencies

## Release channels

- **dev** (pushes to `main`): base `X.Y.(Z+1)`; npm
  `X.Y.(Z+1)-dev.YYYY-MM-DD.HH-MM-SS.<sha7>`; PyPI `X.Y.(Z+1).devYYYYMMDDHHMMSS`; dist
  tag `dev`.
- **nightly** (scheduled): base `X.Y.(Z+1)`; npm `X.Y.(Z+1)-dev.YYYY-MM-DD`; PyPI
  `X.Y.(Z+1).devYYYYMMDD`; dist tag `nightly`.
- **stable** (tag `vX.Y.Z`): publish `X.Y.Z` with dist tag `latest`.

The PyPI Trusted Publisher must reference workflow `publish.yml` and environment `pypi`.
The npm Trusted Publisher must reference workflow `publish.yml` and environment `npm`.

Because published versions are real, breaking the public `h4ckath0n` API is only allowed
through a deliberate version bump on these channels — see
[engineering standards](engineering-standards.md).

## Dependency policy

- Default install includes FastAPI, SQLAlchemy, psycopg, WebAuthn, and the OpenAI SDK.
- LangChain, LangGraph, and LangSmith are dependencies but **not pre-wired**.
- Password auth is an optional extra: `h4ckath0n[password]`.
- Redis is an optional extra that only adds the dependency (no built-in integration).

## Renovate

- Renovate runs via the GitHub App, configured in `renovate.json`.
- Scope: `pyproject.toml` (uv-managed), weekly `uv.lock` maintenance, and GitHub Actions.
- Policy: minor and patch updates may automerge only after CI passes; major updates never
  automerge.
- If the repo gains new ecosystems (Dockerfiles, npm, cargo, Terraform), extend
  `renovate.json` with the right managers and grouping while keeping this automerge policy.

## Keeping dependencies current (uv)

Keep the dependency set healthy and moving forward:

- Periodically run `uv sync --upgrade`.
- Fix compatibility issues by migrating code forward and addressing deprecations.
- Do not downgrade dependencies to make tests pass unless a regression forces it.
- When `uv sync --upgrade` changes `uv.lock`, commit those changes together with the code
  fixes and tests that go with them.
