#!/usr/bin/env node
/**
 * Poll until the backend OpenAPI schema is available.
 * Usage: node scripts/waitForOpenApi.mjs [url] [timeoutMs]
 */

const url = process.argv[2] || "http://127.0.0.1:8000/openapi.json";
const timeout = parseInt(process.argv[3] || "30000", 10);
const interval = 500;
const start = Date.now();

async function poll() {
  while (Date.now() - start < timeout) {
    try {
      const res = await fetch(url);
      if (res.ok) {
        console.log(`✓ OpenAPI schema available at ${url}`);
        return;
      }
    } catch {
      // server not ready yet
    }
    await new Promise((r) => setTimeout(r, interval));
  }
  console.error(`✗ Timed out waiting for ${url} after ${timeout}ms`);
  process.exit(1);
}

poll();
