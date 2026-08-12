import type { EditorialPlan } from "../api.js";

export function EditorialPlanCard({
  plan,
  onApprove,
  onReviseRequest,
  busy,
}: {
  plan: EditorialPlan;
  onApprove: () => void;
  onReviseRequest: () => void;
  busy: boolean;
}) {
  return (
    <div className="card">
      <h2>Editorial Plan</h2>

      {plan.status === "approved" && (
        <span className="badge badge-approved">Approved</span>
      )}
      {plan.status === "revision_requested" && (
        <span className="badge badge-rejected">Revision requested</span>
      )}

      <div className="direction-field">
        <h3>Headline</h3>
        <p>{plan.headline}</p>
      </div>
      <div className="direction-field">
        <h3>Hook</h3>
        <p>{plan.hook}</p>
      </div>
      <div className="direction-field">
        <h3>Key Insights</h3>
        <ul className="lens-list">
          {plan.keyInsights.map((insight) => (
            <li key={insight}>{insight}</li>
          ))}
        </ul>
      </div>
      <div className="direction-field">
        <h3>Practical Takeaway</h3>
        <p>{plan.practicalTakeaway}</p>
      </div>
      <div className="direction-field">
        <h3>Call to Action</h3>
        <p>{plan.ctaDirection}</p>
      </div>

      {plan.status === "proposed" && (
        <div className="button-row">
          <button className="button-primary" onClick={onApprove} disabled={busy}>
            Approve
          </button>
          <button
            className="button-secondary"
            onClick={onReviseRequest}
            disabled={busy}
          >
            Request Revision
          </button>
        </div>
      )}

      {plan.status === "revision_requested" && (
        <div className="button-row">
          <button
            className="button-secondary"
            onClick={onReviseRequest}
            disabled={busy}
          >
            Regenerate Plan
          </button>
        </div>
      )}

      {plan.status === "approved" && (
        <p className="status-line">
          <strong>Editorial Plan Approved.</strong> The next stage is Draft
          generation.
        </p>
      )}
    </div>
  );
}
