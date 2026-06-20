# Agent operating protocol

This protocol is enforced on every coding agent session in this repository. It is the
repo-relevant, language-neutral distillation of the mandated autonomous-agent system
prompt. Persona and language specifics that do not apply to a Python library have been
dropped; the operating discipline below is binding.

## Product context

h4ckath0n is a Python library for shipping hackathon products quickly with secure
defaults: an opinionated FastAPI + SQLAlchemy stack, passkey and device-JWT auth, a thin
OpenAI wrapper, and an npm scaffold CLI for a full stack template. The default path must
stay the safe path. Optimize for a pit of success: minimal code to reach protected
endpoints, predictable conventions over endless knobs.

## Core operating rules

1. **Bounded autonomy.** Operate without asking for permission on reversible, local work
   (editing files, running tests, regenerating artifacts). When faced with ambiguity,
   make the most reasonable technical assumption, document it, and proceed. The only stops
   are the hard boundaries in [AGENTS.md](../../AGENTS.md): irreversible or shared-state
   actions (deleting branches, force pushes, destructive DB ops, publishing) require
   explicit confirmation.
2. **State management.** Maintain and actively update a todo list for any multi-step task
   so you never lose your place. Mark exactly one item in progress at a time and check
   items off as they complete.
3. **Context optimization.** Monitor task scope. When a subtask risks overwhelming the
   context window or needs deep isolated focus (broad codebase search, large refactor
   survey), delegate it to a subagent and work from its summary.
4. **Termination protocol.** Never stop silently. When the objective is verifiably
   complete — all quality gates green — output an explicit completion message and halt to
   await the next directive.

## Per-step output contract

For non-trivial, multi-step work, keep each step legible:

- **Current state:** what you just completed.
- **Assumptions made:** any technical decision you took independently.
- **Plan (only before writing or modifying code):** the type-safety strategy that makes
  invalid states unrepresentable for this change, and any dead code being pruned or large
  file being split (see [engineering standards](engineering-standards.md)).
- **Next action:** the exact tool, command, or subagent you are running now.

Keep this lightweight. It exists to enforce planning before coding, not to pad output —
favor brevity and token efficiency at every step.
