import { useState } from "react";

export function UrlIntakeForm({
  onSubmit,
  submitting,
}: {
  onSubmit: (url: string) => void;
  submitting: boolean;
}) {
  const [url, setUrl] = useState("");

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!url.trim()) return;
    onSubmit(url.trim());
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="field">
        <label htmlFor="source-url">Paste the URL here to get started.</label>
        <input
          id="source-url"
          name="url"
          type="url"
          required
          placeholder="https://example.com/an-article"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={submitting}
        />
      </div>
      <button className="button-primary" type="submit" disabled={submitting}>
        {submitting ? "Analyzing…" : "Continue"}
      </button>
    </form>
  );
}
