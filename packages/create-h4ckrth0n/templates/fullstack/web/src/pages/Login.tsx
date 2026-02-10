import { useState } from "react";
import { useAuth } from "../auth/AuthContext";

export function Login() {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    setError(null);
    setLoading(true);
    try {
      await login();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-sm px-4 py-16">
      <h1 className="text-2xl font-bold">Sign in</h1>
      <p className="mt-2 text-sm text-text-muted">
        Authenticate with your passkey.
      </p>
      {error && (
        <p className="mt-4 rounded-md bg-danger/10 p-3 text-sm text-danger">{error}</p>
      )}
      <button
        onClick={() => void handleLogin()}
        disabled={loading}
        className="mt-6 w-full rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-white hover:bg-primary-hover disabled:opacity-50"
      >
        {loading ? "Signing in…" : "Sign in with passkey"}
      </button>
    </div>
  );
}
