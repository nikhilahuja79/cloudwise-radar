import { useEffect, useState } from "react";
import "./App.css";

type Summary = {
  total_findings: number;
  total_recommendations: number;
  severity_counts: Record<string, number>;
  drift_count: number;
};

type Recommendation = {
  rule_id: string;
  severity: string;
  summary: string;
  explanation: string;
  terraform_fix: string;
  example_fix?: string | null;
};

type DriftFinding = {
  resource: string;
  status: string;
  detected_at: string;
  run_url: string;
};

const API_BASE_URL = "/api";

function App() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [driftFindings, setDriftFindings] = useState<DriftFinding[]>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/summary`)
      .then((response) => response.json())
      .then((data) => setSummary(data));

    fetch(`${API_BASE_URL}/recommendations`)
      .then((response) => response.json())
      .then((data) => setRecommendations(data.items ?? []));

    fetch(`${API_BASE_URL}/drift`)
      .then((response) => response.json())
      .then((data) => setDriftFindings(data.items ?? []));
  }, []);

  return (
    <main className="page">
      <section className="header">
        <div>
          <p className="eyebrow">Azure FinOps + Drift Radar</p>
          <h1>CloudWise Radar</h1>
          <p className="subtitle">
            AI-guided visibility for Terraform drift, cloud cost risks, and remediation.
          </p>
        </div>
      </section>

      <section className="metrics">
        <article>
          <span>Total Findings</span>
          <strong>{summary?.total_findings ?? 0}</strong>
        </article>
        <article>
          <span>AI Recommendations</span>
          <strong>{summary?.total_recommendations ?? 0}</strong>
        </article>
        <article>
          <span>High Severity</span>
          <strong>{summary?.severity_counts?.high ?? 0}</strong>
        </article>
        <article>
          <span>Drift Detected</span>
          <strong>{summary?.drift_count ?? 0}</strong>
        </article>
      </section>

      <section className="panel">
        <div className="panel-heading">
          <h2>Drift Findings</h2>
          <span>{driftFindings.length} items</span>
        </div>

        {driftFindings.length === 0 ? (
          <div className="empty">
            No drift detected. Azure resources match the Terraform state.
          </div>
        ) : (
          <div className="recommendation-list">
            {driftFindings.map((item, index) => (
              <article className="recommendation" key={`${item.resource}-${index}`}>
                <div>
                  <span className="badge high">{item.status}</span>
                  <h3>{item.resource}</h3>
                </div>
                <p>Detected at {item.detected_at}</p>
                <a href={item.run_url} target="_blank" rel="noreferrer">
                  View workflow run
                </a>
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="panel">
        <div className="panel-heading">
          <h2>AI Recommendations</h2>
          <span>{recommendations.length} items</span>
        </div>

        {recommendations.length === 0 ? (
          <div className="empty">
            No active FinOps violations. Your current Terraform baseline is clean.
          </div>
        ) : (
          <div className="recommendation-list">
            {recommendations.map((item, index) => (
              <article className="recommendation" key={`${item.rule_id}-${index}`}>
                <div>
                  <span className={`badge ${item.severity}`}>{item.severity}</span>
                  <h3>{item.summary}</h3>
                </div>
                <p>{item.explanation}</p>
                <pre>{item.terraform_fix}</pre>
                {item.example_fix && <code>{item.example_fix}</code>}
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;