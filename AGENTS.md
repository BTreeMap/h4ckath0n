# AGENTS.md

h4ckath0n is a Python library for shipping hackathon products fast with secure defaults: an
opinionated FastAPI + SQLAlchemy stack, passkey and device-JWT auth, a thin OpenAI wrapper,
and an npm scaffold CLI for a full stack template (api and web).

This file is the minimal entry point. Load the linked agent docs **just in time** — only
when the task needs them — to keep context lean.

## Agent operating protocol

- Work autonomously through reversible steps; make reasonable assumptions, document them,
  and proceed. Pause only for the hard boundaries below.
- Track multi-step work in a todo list, and delegate large or context-heavy subtasks to a
  subagent.
- Never stop silently: announce completion explicitly once all quality gates are green.
- Full protocol and per-step output contract: [docs/agents/operating-protocol.md](docs/agents/operating-protocol.md).

## Tooling and commands

- Backend uses `uv`. Never call `pip` or `python` directly; run via `uv run`.
- Sync: `uv sync --locked --all-extras`
- Agent skills under `.github/skills` are a git submodule tracking
  [BTreeMap/SKILLs](https://github.com/BTreeMap/SKILLs). Clone with
  `git clone --recurse-submodules`, or initialize an existing checkout with
  `git submodule update --init --recursive`. Refresh skills with
  `git submodule update --remote .github/skills`, then commit the bumped pointer.
  Edit skill content upstream in the SKILLs repo, not in this repo.
- Format: `uv run --locked ruff format .`
- CI gate: `uv run --locked ruff format --check . && uv run --locked ruff check . && uv run --locked mypy src && uv run --locked pytest -v`
- Frontend template (from `packages/create-h4ckath0n/templates/fullstack/web/`):
  `npm ci && npm run lint && npm run typecheck && npm test && npm run build`
- Regenerate OpenAPI types after API changes: `npm run gen` (from the web directory).
- All commands, the test surface, E2E, and scaffold checks: [docs/agents/workflows.md](docs/agents/workflows.md).

## Boundaries and constraints

- Authorization is computed server side from DB state. Do not put privilege claims in JWTs;
  enforce access with `require_user()`/`require_admin()`/`require_scopes("a", "b")` from
  [src/h4ckath0n/auth/dependencies.py](src/h4ckath0n/auth/dependencies.py) (re-exported from
  `h4ckath0n.auth`).
- Do not document or reintroduce server-minted access/refresh token flows. The source of
  truth is [docs/security/frontend.md](docs/security/frontend.md); keep auth docs aligned.
- Never use email as a user ID. Use the prefixed base32 generators in
  [src/h4ckath0n/auth/passkeys/ids.py](src/h4ckath0n/auth/passkeys/ids.py).
- Do not revoke a user's last active passkey or weaken its transactional invariant.
- Never log secrets, tokens, Authorization headers, or WebAuthn payloads.
- Do not hand-edit generated artifacts (`api/openapi.json`, `web/src/api/openapi.ts`);
  regenerate them. Do not call `npx` in Node source — use `npm exec --no -- ...`.
- Never break the public `h4ckath0n` API without a deliberate version bump.
- Never commit changes that fail the CI gate above.
- Full security invariants: [docs/agents/security-model.md](docs/agents/security-model.md).

## Engineering standards

- Make invalid states unrepresentable; lean on precise types and a passing `mypy src`.
- Never swallow errors — raise typed exceptions or return typed results; no bare `except`.
- Keep modules cohesive and under ~500 lines; split aggressively and prune internal dead
  code, while preserving the stable public API.
- Python-specific guidance: [docs/agents/engineering-standards.md](docs/agents/engineering-standards.md).

## Domain documentation (load just in time)

- Operating protocol: [docs/agents/operating-protocol.md](docs/agents/operating-protocol.md)
- Engineering standards: [docs/agents/engineering-standards.md](docs/agents/engineering-standards.md)
- Security and auth invariants: [docs/agents/security-model.md](docs/agents/security-model.md)
- Commands, OpenAPI, tests, E2E, scaffold: [docs/agents/workflows.md](docs/agents/workflows.md)
- Releases and dependencies: [docs/agents/release-and-deps.md](docs/agents/release-and-deps.md)
- Commit message rules (Conventional Commits): [.github/skills/git-commits/SKILL.md](.github/skills/git-commits/SKILL.md)
  (managed in the `.github/skills` submodule; see Tooling and commands)
- Canonical reference docs: [docs/index.md](docs/index.md)
