import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Fingerprint, Plus, Trash2, AlertCircle } from "lucide-react";
import { apiClient } from "../api/client";
import type { components } from "../api/generated/schema";
import { toCreateOptions, serializeCreateResponse } from "../auth/webauthn";
import { Card, CardContent, CardHeader } from "../components/Card";
import { Button } from "../components/Button";
import { Alert } from "../components/Alert";

/** Backend-derived type for a passkey record. */
type PasskeyInfo = components["schemas"]["PasskeyInfo"];

export function Settings() {
  const queryClient = useQueryClient();
  const [addLoading, setAddLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastPasskeyError, setLastPasskeyError] = useState<string | null>(null);

  const { data: passkeys, isLoading } = useQuery<PasskeyInfo[]>({
    queryKey: ["passkeys"],
    queryFn: async () => {
      const { data, error } = await apiClient.GET("/auth/passkeys");
      if (error) throw new Error("Failed to load passkeys");
      return data.passkeys;
    },
  });

  const revokeMutation = useMutation({
    mutationFn: async (passkeyId: string) => {
      setLastPasskeyError(null);
      const { response } = await apiClient.POST("/auth/passkeys/{key_id}/revoke", {
        params: { path: { key_id: passkeyId } },
      });
      if (!response.ok) {
        const body = await response.json().catch(() => ({})) as { error?: string; detail?: string | { code?: string; message?: string } };
        const detail = body.detail;
        if (
          body.error === "LAST_PASSKEY" ||
          (typeof detail === "string" && detail.includes("LAST_PASSKEY")) ||
          (typeof detail === "object" && detail?.code === "LAST_PASSKEY")
        ) {
          throw new Error("LAST_PASSKEY");
        }
        const msg = typeof detail === "string" ? detail : (detail as { message?: string })?.message || "Revoke failed";
        throw new Error(msg);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["passkeys"] });
    },
    onError: (err: Error) => {
      if (err.message === "LAST_PASSKEY") {
        setLastPasskeyError(
          "Cannot revoke your last active passkey. Add another passkey first to maintain account access."
        );
      } else {
        setError(err.message);
      }
    },
  });

  const handleAddPasskey = async () => {
    setAddLoading(true);
    setError(null);
    try {
      const { data: startData, error: startError } = await apiClient.POST("/auth/passkey/add/start");
      if (startError || !startData) throw new Error("Failed to start passkey addition");

      const createOptions = toCreateOptions(
        startData.options as unknown as Parameters<typeof toCreateOptions>[0]
      );
      const credential = (await navigator.credentials.create(
        createOptions
      )) as PublicKeyCredential | null;
      if (!credential) throw new Error("Passkey creation cancelled");

      const { error: finishError } = await apiClient.POST("/auth/passkey/add/finish", {
        body: {
          flow_id: startData.flow_id,
          credential: serializeCreateResponse(credential),
        },
      });
      if (finishError) throw new Error("Failed to add passkey");

      queryClient.invalidateQueries({ queryKey: ["passkeys"] });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add passkey");
    } finally {
      setAddLoading(false);
    }
  };

  const activePasskeys = passkeys?.filter((p) => !p.revoked_at) ?? [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text">Settings</h1>
        <p className="text-text-muted">Manage your passkeys and account security</p>
      </div>

      {error && <Alert variant="error" data-testid="settings-error">{error}</Alert>}
      {lastPasskeyError && (
        <Alert variant="warning" data-testid="last-passkey-error">
          <div className="flex items-start gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{lastPasskeyError}</span>
          </div>
        </Alert>
      )}

      <Card>
        <CardHeader className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Fingerprint className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold text-text">Passkeys</h2>
            <span className="text-sm text-text-muted">({activePasskeys.length} active)</span>
          </div>
          <Button size="sm" onClick={handleAddPasskey} disabled={addLoading} data-testid="add-passkey-btn">
            <Plus className="w-4 h-4" />
            {addLoading ? "Adding..." : "Add Passkey"}
          </Button>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-6 w-6 border-2 border-primary border-t-transparent" />
            </div>
          ) : passkeys && passkeys.length > 0 ? (
            <div className="divide-y divide-border">
              {passkeys.map((passkey) => (
                <div key={passkey.id} className="flex items-center justify-between py-3" data-testid="passkey-item">
                  <div>
                    <p className="text-sm font-medium text-text">
                      {passkey.label || "Unnamed passkey"}
                      {passkey.revoked_at && (
                        <span className="ml-2 text-xs text-danger">(revoked)</span>
                      )}
                    </p>
                    <p className="text-xs text-text-muted font-mono">{passkey.id}</p>
                    <p className="text-xs text-text-muted">
                      Created: {new Date(passkey.created_at).toLocaleDateString()}
                      {passkey.last_used_at && (
                        <> | Last used: {new Date(passkey.last_used_at).toLocaleDateString()}</>
                      )}
                    </p>
                  </div>
                  {!passkey.revoked_at && (
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => revokeMutation.mutate(passkey.id)}
                      disabled={revokeMutation.isPending}
                      data-testid="revoke-passkey-btn"
                    >
                      <Trash2 className="w-3 h-3" />
                      Revoke
                    </Button>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-text-muted py-4 text-center">No passkeys found.</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
