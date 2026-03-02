#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/app}"
PYTHON_VERSION="${PYTHON_VERSION:-3.14}"

# Keep installs per-user and avoid editing shell profiles (good for ephemeral CI/Jules envs)
UV_BIN_DIR="${UV_BIN_DIR:-$HOME/.local/bin}"
FNM_DIR="${FNM_DIR:-$HOME/.local/share/fnm}"

log()  { printf "\n==> %s\n" "$*"; }
warn() { printf "\nWARNING: %s\n" "$*" >&2; }
have() { command -v "$1" >/dev/null 2>&1; }

run_or_warn() {
  if ! "$@"; then
    warn "Command failed (continuing): $*"
    return 0
  fi
}

require_root_dir() {
  if [[ ! -d "$ROOT_DIR" ]]; then
    printf "ERROR: ROOT_DIR does not exist: %s\n" "$ROOT_DIR" >&2
    exit 1
  fi
}

npm_install_dir() {
  # Usage: npm_install_dir /path/to/dir
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    return 0
  fi
  if [[ ! -f "$dir/package.json" ]]; then
    return 0
  fi

  log "Installing Node dependencies in $dir"
  if [[ -f "$dir/package-lock.json" ]]; then
    ( cd "$dir" && npm ci )
  else
    # Best effort when there is no lockfile (avoid audit/fund noise)
    ( cd "$dir" && npm install --no-audit --no-fund )
  fi
}

npm_run_if_script_exists() {
  # Usage: npm_run_if_script_exists /path/to/dir scriptName
  local dir="$1"
  local script="$2"
  if [[ ! -f "$dir/package.json" ]]; then
    return 0
  fi

  if node -e "
    const p=require('$dir/package.json');
    process.exit(p.scripts && Object.prototype.hasOwnProperty.call(p.scripts,'$script') ? 0 : 1);
  " >/dev/null 2>&1; then
    log "Running npm script '$script' in $dir"
    ( cd "$dir" && npm run "$script" )
  fi
}

install_uv() {
  log "Installing uv (latest) into $UV_BIN_DIR (unmanaged)"
  mkdir -p "$UV_BIN_DIR"
  if ! have uv; then
    curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="$UV_BIN_DIR" sh
  fi
  export PATH="$UV_BIN_DIR:$PATH"
  log "uv version"
  uv --version
}

install_python() {
  log "Installing Python $PYTHON_VERSION via uv"
  uv python install "$PYTHON_VERSION"
}

install_fnm_node_npm() {
  log "Installing fnm into $FNM_DIR (skip shell modifications)"
  mkdir -p "$FNM_DIR"
  if ! have fnm; then
    curl -fsSL https://fnm.vercel.app/install | bash -s -- --install-dir "$FNM_DIR" --skip-shell
  fi
  export PATH="$FNM_DIR:$PATH"

  # Configure this shell to see the Node selected by fnm
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
}

install_python_deps_with_uv() {
  log "Installing Python dependencies with uv.lock (locked), dev deps, and all extras"

  local py_project_dir=""
  if [[ -f "$ROOT_DIR/pyproject.toml" ]]; then
    py_project_dir="$ROOT_DIR"
  elif [[ -f "$ROOT_DIR/api/pyproject.toml" ]]; then
    py_project_dir="$ROOT_DIR/api"
  fi

  if [[ -z "$py_project_dir" ]]; then
    log "Skipping Python install: no pyproject.toml found at $ROOT_DIR or $ROOT_DIR/api"
    return 0
  fi

  pushd "$py_project_dir" >/dev/null

  if [[ ! -f "uv.lock" ]]; then
    log "No uv.lock found in $py_project_dir. Creating one (uv lock) so we can do a locked sync."
    uv lock
  fi

  # Notes:
  # - --locked enforces that uv.lock matches pyproject.toml
  # - dev group is synced by default by uv sync
  # - --all-extras installs every optional dependency extra
  uv sync --locked --all-extras

  popd >/dev/null
}

install_node_deps_upstream_or_downstream() {
  log "Installing Node dependencies (handle upstream h4ckath0n repo and downstream generated apps)"

  local upstream_scaffolder_dir="$ROOT_DIR/packages/create-h4ckath0n"
  local upstream_template_web_dir="$ROOT_DIR/packages/create-h4ckath0n/templates/fullstack/web"
  local downstream_web_dir="$ROOT_DIR/web"

  local is_upstream="false"
  if [[ -f "$upstream_scaffolder_dir/package.json" ]] || [[ -d "$ROOT_DIR/packages/create-h4ckath0n/templates" ]]; then
    is_upstream="true"
  fi

  local is_downstream="false"
  if [[ -f "$downstream_web_dir/package.json" ]] || [[ -f "$downstream_web_dir/package-lock.json" ]]; then
    is_downstream="true"
  fi

  if [[ "$is_upstream" == "true" ]]; then
    log "Detected upstream h4ckath0n repo layout under $ROOT_DIR"

    # Scaffolder deps
    npm_install_dir "$upstream_scaffolder_dir"

    # Fullstack web template deps + OpenAPI typegen (if present)
    npm_install_dir "$upstream_template_web_dir"
    npm_run_if_script_exists "$upstream_template_web_dir" "gen"
  fi

  if [[ "$is_downstream" == "true" ]]; then
    log "Detected downstream project layout (frontend in $downstream_web_dir)"

    npm_install_dir "$downstream_web_dir"
    npm_run_if_script_exists "$downstream_web_dir" "gen"
  fi

  if [[ "$is_upstream" != "true" && "$is_downstream" != "true" ]]; then
    log "No known Node project layout detected."
    log "Checked: $upstream_scaffolder_dir, $upstream_template_web_dir, and $downstream_web_dir"
  fi
}

main() {
  require_root_dir

  # 0) Basic OS tools (best effort). If you do not have sudo/apt-get, this silently skips.
  log "Ensuring basic OS tools (best effort)"
  if have apt-get; then
    if have sudo; then
      run_or_warn sudo apt-get update -y
      run_or_warn sudo env DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
      run_or_warn sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates curl git unzip jq ripgrep build-essential
    else
      run_or_warn apt-get update -y
      run_or_warn env DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
      run_or_warn env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates curl git unzip jq ripgrep build-essential
    fi
  fi

  mkdir -p "$UV_BIN_DIR" "$FNM_DIR"

  # 1) uv
  install_uv

  # 2) Python via uv (no fallback)
  install_python

  # 3) fnm + Node LTS + npm latest
  install_fnm_node_npm

  # 4) Python deps via uv.lock (locked), dev deps (default), all extras
  install_python_deps_with_uv

  # 5) Node deps: upstream repo and/or downstream generated projects
  install_node_deps_upstream_or_downstream

  log "Done. Suggested quick checks (adjust paths for downstream projects):"
  cat <<EOF
  - Backend tests:  (cd "$ROOT_DIR" && uv run --locked pytest -v)   # or (cd "$ROOT_DIR/api" && ...)
  - Lint:          (cd "$ROOT_DIR" && uv run --locked ruff check .)
  - Types:         (cd "$ROOT_DIR" && uv run --locked mypy src)

  - Upstream web template:
      (cd "$ROOT_DIR/packages/create-h4ckath0n/templates/fullstack/web" && npm run check)

  - Downstream web:
      (cd "$ROOT_DIR/web" && npm run check)

  - E2E (if you need it):
      (cd "<web_dir>" && npx playwright install --with-deps chromium && npx playwright test)
EOF
}

main "$@"
