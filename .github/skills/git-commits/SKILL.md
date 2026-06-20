---
name: git-commit-standards
description: Enforces Conventional Commits format and best practices. Use this skill whenever drafting, reviewing, or validating git commit messages for the repository.
---

# Git Commit Message Standards

You must adhere strictly to the Conventional Commits specification. A clean, structured commit history ensures accurate changelog generation, easier debugging, and rapid code reviews.

## 1. Commit Message Anatomy
Every commit message must follow this exact schema:

```text
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

## 2. Subject Line Rules

The subject line contains the `<type>`, `<scope>`, and `<subject>` description.

* **Length Constraint:** The entire subject line must be **strictly 70 characters or less**.
* **Type:** Must be lowercase and chosen from the approved list below.
* **Scope:** Optional, but highly recommended. Must be lowercase, enclosed in parentheses, and represent the specific domain or component modified (e.g., `auth`, `ui`, `db`).
* **Imperative Mood:** The subject description must act as a command (e.g., "Add feature", "Fix bug", "Refactor logic"). Never use past or present continuous tense ("Added", "Adding").
* **Formatting:** Capitalize the first letter of the subject description. Do not end the line with a period.

## 3. Approved Types

* **`feat`**: Introduces a new feature to the codebase.
* **`fix`**: Patches a bug or addresses an error.
* **`refactor`**: Modifies code without changing external behavior or adding features (e.g., renaming variables, simplifying logic).
* **`docs`**: Updates documentation, READMEs, or inline comments.
* **`style`**: Adjusts code formatting, whitespace, or missing semicolons (no logic changes).
* **`perf`**: Improves performance and execution speed.
* **`test`**: Adds missing tests or corrects existing ones.
* **`build`**: Modifies build systems or external dependencies (e.g., npm, webpack).
* **`ci`**: Updates continuous integration configurations or scripts (e.g., GitHub Actions).
* **`chore`**: Handles routine maintenance tasks that do not modify source or test files.
* **`revert`**: Reverts a previous commit.

## 4. Body Rules

The body provides the context necessary to understand the structural reasoning behind the commit.

* **Separation:** Always separate the subject line and the body with a single blank line.
* **Line Wrapping:** Wrap all lines in the body at **72 characters** to maintain terminal readability.
* **Content:** Explain the **"what"** and the **"why"**. Detail the problem being solved and the rationale behind the chosen solution. Omit the "how", as the exact implementation details are inherently visible in the code diff.

## 5. Footer Rules (Optional)

* Use the footer to reference issue trackers (e.g., `Fixes #123`, `Resolves #456`).
* Highlight breaking changes by starting the footer with `BREAKING CHANGE:` followed by a space or two empty lines and a detailed description of the migration path.

## 6. Examples

### Valid Implementation

```text
feat(auth): Implement JWT token refresh mechanism

The current authentication flow forces users to log out after 1 hour
when their session expires. This introduces a background token refresh
worker to seamlessly renew the session without interrupting the user.

Resolves #89
```

### Invalid Implementation (Do Not Produce)

```text
fixed the bug
added a token refresh thing so users dont get logged out randomly anymore. also updated the ui to show a loading spinner while it happens
```

* **Violations:** Missing type, missing scope, past tense, missing blank line, missing capitalization, body lines exceed 72 characters, missing issue reference.
