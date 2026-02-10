#!/usr/bin/env node
/**
 * Full-stack development orchestrator.
 *
 * 1. Starts the backend (uvicorn via uv run)
 * 2. Waits for /openapi.json to become available
 * 3. Runs initial codegen
 * 4. Watches backend source files and re-runs codegen on changes
 * 5. Starts Vite dev server
 *
 * Usage: node scripts/devFullstack.mjs
 */

import { spawn, execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const apiDir = path.resolve(root, "..", "api");
const openApiUrl = "http://127.0.0.1:8000/openapi.json";

// ── 1. Start backend ──────────────────────────────────────────────
console.log("▶ Starting backend…");
const backend = spawn(
  "uv",
  ["run", "uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"],
  { cwd: apiDir, stdio: "inherit" },
);

backend.on("error", (err) => {
  console.error("✗ Failed to start backend:", err.message);
  process.exit(1);
});

// Clean up on exit
function cleanup() {
  backend.kill("SIGTERM");
}
process.on("SIGINT", cleanup);
process.on("SIGTERM", cleanup);
process.on("exit", cleanup);

// ── 2. Wait for OpenAPI ───────────────────────────────────────────
console.log("▶ Waiting for OpenAPI schema…");
execFileSync("node", [path.join(root, "scripts", "waitForOpenApi.mjs"), openApiUrl, "30000"], {
  cwd: root,
  stdio: "inherit",
});

// ── 3. Initial codegen ────────────────────────────────────────────
console.log("▶ Running initial codegen…");
execFileSync("node", [path.join(root, "scripts", "genApi.mjs"), openApiUrl], {
  cwd: root,
  stdio: "inherit",
});

// ── 4. Watch backend for changes & regenerate ─────────────────────
async function startWatcher() {
  const { watch } = await import("chokidar");
  const watcher = watch(path.join(apiDir, "**/*.py"), {
    ignoreInitial: true,
    awaitWriteFinish: { stabilityThreshold: 500 },
  });

  let debounce = null;
  watcher.on("all", () => {
    if (debounce) clearTimeout(debounce);
    debounce = setTimeout(() => {
      console.log("▶ Backend changed, regenerating types…");
      try {
        // Wait a moment for uvicorn --reload to restart
        execFileSync("node", [path.join(root, "scripts", "waitForOpenApi.mjs"), openApiUrl, "15000"], {
          cwd: root,
          stdio: "inherit",
        });
        execFileSync("node", [path.join(root, "scripts", "genApi.mjs"), openApiUrl], {
          cwd: root,
          stdio: "inherit",
        });
      } catch {
        console.warn("⚠ Codegen failed after backend change, will retry on next change");
      }
    }, 2000);
  });
}

startWatcher();

// ── 5. Start Vite ─────────────────────────────────────────────────
console.log("▶ Starting Vite…");
const vite = spawn("npx", ["vite"], { cwd: root, stdio: "inherit" });

vite.on("exit", (code) => {
  cleanup();
  process.exit(code ?? 0);
});
