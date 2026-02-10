/**
 * Typed API client – single source of truth for all backend calls.
 *
 * Built on `openapi-fetch` and auto-generated OpenAPI types so that
 * request/response shapes stay in sync with the backend at compile time.
 *
 * All API calls in this template should go through `apiClient` (authenticated)
 * or `publicApiClient` (unauthenticated, for login/register).
 */

import createClient, { type Middleware } from "openapi-fetch";
import type { paths } from "./generated/schema";
import { getOrMintToken, clearCachedToken } from "../auth/token";
import { getDeviceIdentity } from "../auth/deviceKey";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

/**
 * Middleware that attaches a device-key JWT to every request.
 * On 401 the cached token is cleared so the next call will re-mint.
 */
const authMiddleware: Middleware = {
  async onRequest({ request }) {
    const identity = await getDeviceIdentity();
    if (!identity) {
      throw new Error("Not authenticated");
    }
    const token = await getOrMintToken("http");
    request.headers.set("Authorization", `Bearer ${token}`);
    return request;
  },
  async onResponse({ response }) {
    if (response.status === 401) {
      clearCachedToken();
    }
    return response;
  },
};

/** Authenticated client – use for all endpoints that require auth. */
export const apiClient = createClient<paths>({ baseUrl: API_BASE });
apiClient.use(authMiddleware);

/** Public client – use for unauthenticated endpoints (register/login). */
export const publicApiClient = createClient<paths>({ baseUrl: API_BASE });
