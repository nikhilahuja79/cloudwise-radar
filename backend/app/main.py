import json
from pathlib import Path
from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = ROOT / "outputs"
FINDINGS_FILE = OUTPUTS_DIR / "finops-findings.json"
RECOMMENDATIONS_FILE = OUTPUTS_DIR / "ai-recommendations.json"

app = FastAPI(
    title="CloudWise Radar API",
    description="API for FinOps findings, Terraform drift status, and AI recommendations.",
    version="0.1.0",
)


def read_json_file(path: Path):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "cloudwise-radar-api",
    }


@app.get("/findings")
def findings():
    return {
        "items": read_json_file(FINDINGS_FILE),
    }


@app.get("/recommendations")
def recommendations():
    return {
        "items": read_json_file(RECOMMENDATIONS_FILE),
    }


@app.get("/summary")
def summary():
    findings_data = read_json_file(FINDINGS_FILE)
    recommendations_data = read_json_file(RECOMMENDATIONS_FILE)

    severity_counts = {}
    for finding in findings_data:
        severity = finding.get("severity", "unknown")
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    return {
        "total_findings": len(findings_data),
        "total_recommendations": len(recommendations_data),
        "severity_counts": severity_counts,
    }