import { useState } from "react";
import { useAuth } from "../auth/AuthContext";

export function Register() {
  const { register } = useAuth();
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleRegister() {
    setError(null);
    setLoading(true);
    try {
      await register(displayName || "User");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-sm px-4 py-16">
      <h1 className="text-2xl font-bold">Create account</h1>
      <p className="mt-2 text-sm text-text-muted">
        Register with a passkey — no password needed.
      </p>
      {error && (
        <p className="mt-4 rounded-md bg-danger/10 p-3 text-sm text-danger">{error}</p>
      )}
      <input
        type="text"
        placeholder="Display name"
        value={displayName}
        onChange={(e) => setDisplayName(e.target.value)}
        className="mt-6 w-full rounded-lg border border-border bg-surface px-4 py-2.5 text-sm"
      />
      <button
        onClick={() => void handleRegister()}
        disabled={loading}
        className="mt-4 w-full rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-white hover:bg-primary-hover disabled:opacity-50"
      >
        {loading ? "Creating…" : "Register with passkey"}
      </button>
    </div>
  );
}
