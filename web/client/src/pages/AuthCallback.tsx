import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { api, ApiError } from "../api.js";

export function AuthCallback({ onSignedIn }: { onSignedIn: () => Promise<void> }) {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const token = searchParams.get("token");

  useEffect(() => {
    if (!token) {
      setError("This sign-in link is missing its token.");
      return;
    }
    let cancelled = false;
    api
      .completeMagicLink(token)
      .then(async () => {
        if (cancelled) return;
        await onSignedIn();
        navigate("/", { replace: true });
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err instanceof ApiError ? err.message : "Sign-in failed.");
      });
    return () => {
      cancelled = true;
    };
  }, [token, navigate, onSignedIn]);

  return (
    <div className="page">
      <div className="card">
        {error ? (
          <>
            <h2>Sign-in link problem</h2>
            <div className="error-banner">{error}</div>
            <a href="/sign-in">Request a new link</a>
          </>
        ) : (
          <p className="status-line">Signing you in…</p>
        )}
      </div>
    </div>
  );
}
