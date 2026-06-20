# Agent documentation

This directory holds the operational manual for AI coding agents working on h4ckath0n.
The root [AGENTS.md](../../AGENTS.md) stays intentionally small; load the documents below
just in time, only when the task at hand needs them.

## Map

- [Operating protocol](operating-protocol.md) — how an agent runs a session: autonomy,
  state tracking, subagent delegation, termination, and the per-step output contract.
- [Engineering standards](engineering-standards.md) — Python-adapted PLT discipline:
  make invalid states unrepresentable, typed error handling, modularization, pruning.
- [Security model](security-model.md) — the opinionated auth, authorization, identity,
  and secrecy invariants that must be preserved.
- [Workflows](workflows.md) — exact commands and numbered procedures for the CI gate,
  OpenAPI regeneration, frontend template checks, E2E, scaffold CLI, and testing.
- [Releases and dependencies](release-and-deps.md) — release channels, dependency
  policy, Renovate scope, and how to keep the lockfile moving forward.

## Canonical reference docs

The deep, human-facing reference set lives one level up in [docs/index.md](../index.md).
The agent docs here point into those references rather than duplicating them.
