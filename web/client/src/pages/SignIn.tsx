import { useState } from "react";
import { api, ApiError } from "../api.js";

export function SignIn() {
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await api.requestMagicLink(email);
      setSent(true);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  if (sent) {
    return (
      <div className="page">
        <div className="card">
          <h2>Check your email</h2>
          <p className="status-line">
            If an account exists for <strong>{email}</strong>, a sign-in link
            has been sent. It is valid for 15 minutes.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="card">
        <h2>Sign in</h2>
        {error && <div className="error-banner">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="email">Email address</label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
          </div>
          <button className="button-primary" type="submit" disabled={submitting}>
            {submitting ? "Sending…" : "Send sign-in link"}
          </button>
        </form>
      </div>
    </div>
  );
}
