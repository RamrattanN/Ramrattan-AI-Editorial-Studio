import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { type ProjectView, api, ApiError } from "../api.js";
import { EditorialDirectionCard } from "../components/EditorialDirectionCard.js";
import { UrlIntakeForm } from "../components/UrlIntakeForm.js";

export function Project() {
  const { id } = useParams<{ id: string }>();
  const [view, setView] = useState<ProjectView | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    if (!id) return;
    try {
      const next = await api.getProject(id);
      setView(next);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not load project.");
    }
  }, [id]);

  useEffect(() => {
    void load();
  }, [load]);

  async function handleSubmitUrl(url: string) {
    if (!id) return;
    setProcessing(true);
    setError(null);
    try {
      await api.submitSource(id, url);
      await load();
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "The source could not be processed. Please try again.",
      );
    } finally {
      setProcessing(false);
    }
  }

  async function handleApprove() {
    if (!id) return;
    setBusy(true);
    setError(null);
    try {
      await api.approveDirection(id);
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not approve.");
    } finally {
      setBusy(false);
    }
  }

  async function handleReject(feedback: string) {
    if (!id) return;
    setBusy(true);
    setError(null);
    try {
      await api.rejectDirection(id, feedback);
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not submit feedback.");
    } finally {
      setBusy(false);
    }
  }

  if (!view) {
    return (
      <div className="page">
        {error ? <div className="error-banner">{error}</div> : <p className="status-line">Loading…</p>}
      </div>
    );
  }

  return (
    <div className="page">
      {error && <div className="error-banner">{error}</div>}

      <div className="card">
        <h2>{view.project.title}</h2>
        <p className="status-line">{view.project.id}</p>
      </div>

      {!view.editorialDirection && (
        <div className="card">
          <UrlIntakeForm onSubmit={handleSubmitUrl} submitting={processing} />
          {processing && (
            <p className="status-line" style={{ marginTop: "0.75rem" }}>
              Retrieving the source and preparing an Editorial Direction…
            </p>
          )}
        </div>
      )}

      {view.source && view.source.retrievalStatus === "failed" && (
        <div className="card">
          <div className="error-banner">{view.source.retrievalError}</div>
        </div>
      )}

      {view.editorialDirection && (
        <EditorialDirectionCard
          direction={view.editorialDirection}
          onApprove={handleApprove}
          onReject={handleReject}
          busy={busy}
        />
      )}
    </div>
  );
}
