#!/usr/bin/env node
/**
 * Generate TypeScript types from the backend OpenAPI schema.
 * Usage: node scripts/genApi.mjs [url]
 *
 * Fetches the OpenAPI JSON from the running backend and writes
 * deterministic TypeScript types to src/api/generated/schema.ts.
 */

import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const url = process.argv[2] || "http://127.0.0.1:8000/openapi.json";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outFile = path.join(root, "src", "api", "generated", "schema.ts");

try {
  execFileSync(
    "npx",
    ["--yes", `openapi-typescript@7.12.0`, url, "-o", outFile],
    { cwd: root, stdio: "inherit" },
  );
  console.log(`✓ Generated ${path.relative(root, outFile)}`);
} catch (err) {
  console.error("✗ OpenAPI codegen failed:", err.message);
  process.exit(1);
}
