import { useState } from "react";
import type { EditorialDirection } from "../api.js";

export function EditorialDirectionCard({
  direction,
  onApprove,
  onReject,
  busy,
}: {
  direction: EditorialDirection;
  onApprove: () => void;
  onReject: (feedback: string) => void;
  busy: boolean;
}) {
  const [feedback, setFeedback] = useState(direction.rejectFeedback ?? "");
  const [showRejectField, setShowRejectField] = useState(
    direction.status === "rejected",
  );

  return (
    <div className="card">
      <h2>Editorial Direction</h2>

      {direction.status === "approved" && (
        <span className="badge badge-approved">Approved</span>
      )}
      {direction.status === "rejected" && (
        <span className="badge badge-rejected">Changes requested</span>
      )}

      <div className="direction-field">
        <h3>Source Understanding</h3>
        <p>{direction.sourceUnderstanding}</p>
      </div>
      <div className="direction-field">
        <h3>Audience</h3>
        <p>{direction.audience}</p>
      </div>
      <div className="direction-field">
        <h3>Objective</h3>
        <p>{direction.objective}</p>
      </div>
      <div className="direction-field">
        <h3>Publication Language</h3>
        <p>{direction.publicationLanguage}</p>
      </div>
      <div className="direction-field">
        <h3>Primary Angle</h3>
        <p>{direction.primaryAngle}</p>
      </div>
      {direction.supportingLenses.length > 0 && (
        <div className="direction-field">
          <h3>Supporting Lenses</h3>
          <ul className="lens-list">
            {direction.supportingLenses.map((lens) => (
              <li key={lens}>{lens}</li>
            ))}
          </ul>
        </div>
      )}
      <div className="direction-field">
        <h3>Editorial Thesis</h3>
        <p>{direction.editorialThesis}</p>
      </div>

      {direction.status === "proposed" && (
        <div className="button-row">
          <button className="button-primary" onClick={onApprove} disabled={busy}>
            Approve
          </button>
          <button
            className="button-secondary"
            onClick={() => setShowRejectField(true)}
            disabled={busy}
          >
            Reject
          </button>
        </div>
      )}

      {direction.status === "approved" && (
        <p className="status-line">
          <strong>Editorial Direction Approved.</strong> The next stage will be
          Editorial Plan.
        </p>
      )}

      {showRejectField && direction.status !== "approved" && (
        <div className="field" style={{ marginTop: "1rem" }}>
          <label htmlFor="reject-feedback">What would you like to change?</label>
          <textarea
            id="reject-feedback"
            rows={3}
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            disabled={busy}
          />
          <div className="button-row">
            <button
              className="button-secondary"
              onClick={() => onReject(feedback)}
              disabled={busy}
            >
              {direction.status === "rejected" ? "Update feedback" : "Submit feedback"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
