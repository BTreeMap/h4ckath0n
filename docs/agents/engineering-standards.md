# Engineering standards

Python-adapted engineering discipline for this repository. The spirit is
Programming-Language-Theory purism — type safety, zero-cost-as-possible abstractions, and
correctness by construction — applied within Python's type system and tooling. Style
(formatting, naming) is enforced deterministically by `ruff` and is not restated here.

## Universal directives

- **Make invalid states unrepresentable.** Encode invariants in the type system so `mypy`
  rejects bad states at check time. Prefer precise types over `Any`, `Enum`/`Literal` over
  bare strings, `pydantic` models and typed dataclasses over loose dicts, and exhaustive
  `match` over open-ended branching. Validate untrusted input only at system boundaries
  (request handlers, env config, DB edges), then carry strong types inward.
- **Idiomatic error handling.** Never swallow errors. No bare `except:` and no
  `except Exception` that hides failures. Raise specific, typed exceptions or return an
  explicit typed result; let `Result`/`Option`-style intent be visible in signatures via
  precise return types (e.g. `X | None`). Errors surfaced to clients must not leak secrets.
- **Aggressive modularization.** Keep modules cohesive and under ~500 lines. When a file
  approaches that limit, autonomously split it into smaller, single-responsibility modules
  rather than letting it grow. This mirrors the existing `src/h4ckath0n/` package layout.
- **Ruthless refactoring of internals, with a stable public surface.** Prune dead code and
  rewrite poorly shaped internal interfaces freely — clean architecture wins. The one
  exception is the **public `h4ckath0n` API**, which is a stability contract: breaking it
  requires a deliberate version bump through the release channels (see
  [releases and dependencies](release-and-deps.md)). Internal churn is free; public churn
  is versioned.

## Python-specific guidance

- **Typing is a compile-time guarantee.** `uv run --locked mypy src` must pass with no new
  ignores. Treat `# type: ignore` as a last resort that needs justification.
- **Zero-cost-as-possible abstractions.** Prefer standard library and already-vendored
  dependencies over new ones. Favor generators and lazy iteration on hot paths; avoid
  materializing large intermediate collections needlessly.
- **No connection or session leaks.** Database sessions must close reliably; do not add
  blocking network calls in the request path unless documented.
- **Effects at the boundary.** Keep pure logic separate from I/O. Push side effects (DB,
  network, filesystem) to the edges so core logic stays easy to test and reason about.
- **Tests prove the invariants.** Every behavioral change ships with `pytest` coverage.
  See [workflows](workflows.md) for the required test surface and the full CI gate.
