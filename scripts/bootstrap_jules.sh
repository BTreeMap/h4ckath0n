#!/usr/bin/env bash
set -euo pipefail

PYTHON_VERSION="${PYTHON_VERSION:-3.11}"

# Keep installs per-user and avoid editing shell profiles (good for ephemeral CI/Jules envs)
UV_BIN_DIR="${UV_BIN_DIR:-$HOME/.local/bin}"
FNM_DIR="${FNM_DIR:-$HOME/.local/share/fnm}"

log() { printf "\n==> %s\n" "$*"; }

have() { command -v "$1" >/dev/null 2>&1; }

# 0) Basic OS tools (best effort). If you do not have sudo/apt-get, this silently skips.
log "Ensuring basic OS tools (best effort)"
if have apt-get; then
  if have sudo; then
    sudo apt-get update -y
    sudo apt-get install -y --no-install-recommends \
      ca-certificates curl git unzip jq ripgrep build-essential
  else
    apt-get update -y || true
    apt-get install -y --no-install-recommends \
      ca-certificates curl git unzip jq ripgrep build-essential || true
  fi
fi

mkdir -p "$UV_BIN_DIR" "$FNM_DIR"

# 1) Install uv (latest) via official installer script, unmanaged so it does not edit profiles
log "Installing uv (latest) into $UV_BIN_DIR (unmanaged)"
if ! have uv; then
  curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="$UV_BIN_DIR" sh
fi
export PATH="$UV_BIN_DIR:$PATH"

log "uv version"
uv --version

# 2) Install Python 3.11 (managed by uv)
log "Installing Python $PYTHON_VERSION via uv"
uv python install "$PYTHON_VERSION" || true

# 3) Install fnm (skip shell modifications), then Node LTS and npm latest
log "Installing fnm into $FNM_DIR (skip shell modifications)"
if ! have fnm; then
  curl -fsSL https://fnm.vercel.app/install | bash -s -- --install-dir "$FNM_DIR" --skip-shell
fi
export PATH="$FNM_DIR:$PATH"

# Configure this shell to see the Node selected by fnm
# (fnm prints shell code; eval wires PATH/shims for the current shell)
eval "$(fnm env --use-on-cd --shell bash)"

log "Installing Node LTS and using it immediately"
fnm install --lts --use

log "Node and npm versions (pre-upgrade)"
node -v
npm -v

log "Upgrading npm to latest"
npm install -g npm@latest

log "Node and npm versions (post-upgrade)"
node -v
npm -v

# 4) Python deps: prefer locked install with dev group + all extras.
# If we are in a generated app layout, use api/ as the Python project.
log "Installing Python dependencies with uv.lock, dev deps, and all extras"

PY_PROJECT_DIR=""
if [[ -f "pyproject.toml" ]]; then
  PY_PROJECT_DIR="."
elif [[ -f "api/pyproject.toml" ]]; then
  PY_PROJECT_DIR="api"
fi

if [[ -n "$PY_PROJECT_DIR" ]]; then
  pushd "$PY_PROJECT_DIR" >/dev/null

  if [[ ! -f "uv.lock" ]]; then
    log "No uv.lock found in $PY_PROJECT_DIR. Creating one (uv lock) so we can do a locked sync."
    uv lock
  fi

  # --all-extras installs every optional-deps extra (e.g., redis, password)
  # dev group is synced by default, but --dev makes intent explicit
  uv sync --locked --all-extras --dev

  popd >/dev/null
else
  log "Skipping Python install: no pyproject.toml found at repo root or ./api"
fi

# 5) Node deps for this repo (scaffolder + web template)
log "Installing Node dependencies (npm ci where lockfiles exist)"

if [[ -f "packages/create-h4ckath0n/package-lock.json" ]]; then
  ( cd packages/create-h4ckath0n && npm ci )
fi

WEB_TEMPLATE_DIR="packages/create-h4ckath0n/templates/fullstack/web"
if [[ -f "$WEB_TEMPLATE_DIR/package-lock.json" ]]; then
  ( cd "$WEB_TEMPLATE_DIR" && npm ci && npm run gen )
fi

log "Done. Suggested quick checks:"
cat <<'EOF'
  - Backend:  uv run --locked pytest -v
  - Lint:     uv run --locked ruff check .
  - Types:    uv run --locked mypy src
  - Web:      (cd packages/create-h4ckath0n/templates/fullstack/web && npm run check)
  - E2E:      (cd packages/create-h4ckath0n/templates/fullstack/web && npx playwright install --with-deps chromium && npx playwright test)
EOF
