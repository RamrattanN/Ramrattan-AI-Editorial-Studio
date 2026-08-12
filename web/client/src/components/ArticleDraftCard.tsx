import type { Article } from "../api.js";

export function ArticleDraftCard({ article }: { article: Article }) {
  return (
    <div className="card">
      <h2>Draft</h2>
      <span className="badge badge-approved">Generated</span>

      <div className="direction-field">
        <h3>Headline</h3>
        <p>{article.headline}</p>
      </div>
      <div className="direction-field">
        <h3>Hook</h3>
        <p>{article.hook}</p>
      </div>
      <div className="direction-field">
        <h3>Key Insights</h3>
        <ul className="lens-list">
          {article.keyInsights.map((insight) => (
            <li key={insight}>{insight}</li>
          ))}
        </ul>
      </div>
      <div className="direction-field">
        <h3>Practical Takeaway</h3>
        <p>{article.practicalTakeaway}</p>
      </div>
      <div className="direction-field">
        <h3>Call to Action</h3>
        <p>{article.cta}</p>
      </div>
      <div className="direction-field">
        <h3>Article</h3>
        <pre className="article-markdown">{article.articleMarkdown}</pre>
      </div>
      {article.sourceAttributions.length > 0 && (
        <div className="direction-field">
          <h3>Sources and Attribution</h3>
          <ul className="lens-list">
            {article.sourceAttributions.map((attribution) => (
              <li key={attribution.citation}>{attribution.citation}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
