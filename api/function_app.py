import json
from pathlib import Path
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
FINDINGS_FILE = DATA_DIR / "finops-findings.json"
RECOMMENDATIONS_FILE = DATA_DIR / "ai-recommendations.json"


def read_json_file(path: Path):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def json_response(payload, status_code=200):
    return func.HttpResponse(
        json.dumps(payload),
        status_code=status_code,
        mimetype="application/json",
    )


@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return json_response({
        "status": "ok",
        "service": "cloudwise-radar-api",
        "runtime": "azure-functions",
    })


@app.route(route="findings", methods=["GET"])
def findings(req: func.HttpRequest) -> func.HttpResponse:
    return json_response({
        "items": read_json_file(FINDINGS_FILE),
    })


@app.route(route="recommendations", methods=["GET"])
def recommendations(req: func.HttpRequest) -> func.HttpResponse:
    return json_response({
        "items": read_json_file(RECOMMENDATIONS_FILE),
    })


@app.route(route="summary", methods=["GET"])
def summary(req: func.HttpRequest) -> func.HttpResponse:
    findings_data = read_json_file(FINDINGS_FILE)
    recommendations_data = read_json_file(RECOMMENDATIONS_FILE)

    severity_counts = {}
    for finding in findings_data:
        severity = finding.get("severity", "unknown")
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    return json_response({
        "total_findings": len(findings_data),
        "total_recommendations": len(recommendations_data),
        "severity_counts": severity_counts,
    })