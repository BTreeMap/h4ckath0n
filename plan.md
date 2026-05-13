1. **Create `scripts/generate_env_docs.py`**
   - Implement the script to parse `src/h4ckath0n/config.py` using Pydantic, and generate the Markdown table for environment variables.
   - It will support `--check` to verify the README is up to date, and `--update` to rewrite the README with the generated table between `<!-- BEGIN ENV VARS -->` and `<!-- END ENV VARS -->` markers.

2. **Update `src/h4ckath0n/config.py`**
   - Add `from pydantic import Field` to the file.
   - Update the `Settings` class to use `Field(description="...")` for all settings, to provide docstrings that will be pulled into the README.

3. **Update `README.md`**
   - Replace the hand-written table with the `<!-- BEGIN ENV VARS -->` and `<!-- END ENV VARS -->` markers.
   - Run `uv run scripts/generate_env_docs.py --update` to inject the generated table.

4. **Add CI Check in `.github/workflows/ci.yml`**
   - Add a step to run `uv run scripts/generate_env_docs.py --check` in the backend job to ensure environment variables drift check is performed in CI.

5. **Log Atlas critical learning**
   - Update `.jules/atlas.md` with an entry explaining that the repo's Pydantic settings are the source of truth for config, and a drift-prevention script is needed to keep the README table up to date.

6. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.**
   - Run `pre_commit_instructions` and follow them.

7. **Submit the PR**
   - Call the `submit` tool to push changes to a branch and submit the PR.
