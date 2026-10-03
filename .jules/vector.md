## 2025-02-13 - Pydantic V2 Annotated Imports
**Learning:** In this repository, `ruff format` does not sort imports. When using Pydantic V2 `Annotated` aliases to centralize validation logic, the added imports (e.g. `from typing import Annotated`) will trigger `I001` from `ruff check`.
**Action:** Always follow formatting with `uv run --locked ruff check --fix .` to auto-sort imports before finalizing Python patches.
