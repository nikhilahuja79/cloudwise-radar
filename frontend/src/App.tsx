import { useEffect, useState } from "react";
import "./App.css";

type Summary = {
  total_findings: number;
  total_recommendations: number;
  severity_counts: Record<string, number>;
};

type Recommendation = {
  rule_id: string;
  severity: string;
  summary: string;
  explanation: string;
  terraform_fix: string;
  example_fix?: string | null;
};

const API_BASE_URL = "/api";

function App() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/summary`)
      .then((response) => response.json())
      .then((data) => setSummary(data));

    fetch(`${API_BASE_URL}/recommendations`)
      .then((response) => response.json())
      .then((data) => setRecommendations(data.items ?? []));
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