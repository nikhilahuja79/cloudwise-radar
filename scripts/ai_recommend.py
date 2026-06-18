import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDINGS_FILE = ROOT / "outputs" / "finops-findings.json"
RECOMMENDATIONS_FILE = ROOT / "outputs" / "ai-recommendations.json"


def recommendation_for_finding(finding):
    rule_id = finding.get("rule_id")

    if rule_id == "FINOPS_TAGS_001":
        return {
            "rule_id": rule_id,
            "severity": finding.get("severity", "high"),
            "summary": "Required FinOps tag is missing.",
            "explanation": (
                "Missing tags reduce cost accountability and make it harder "
                "to identify which team, owner, or environment created spend."
            ),
            "terraform_fix": (
                "Add the missing tag to the common_tags local value or to the "
                "resource-level tags block."
            ),
            "example_fix": 'owner = "team-name"',
        }

    if rule_id == "FINOPS_REGION_001":
        return {
            "rule_id": rule_id,
            "severity": finding.get("severity", "medium"),
            "summary": "Azure region is not approved.",
            "explanation": (
                "Unapproved regions can increase latency, cost, compliance risk, "
                "and operational complexity."
            ),
            "terraform_fix": (
                "Change the Terraform location variable to one of the approved "
                "regions in policies/finops-rules.yaml."
            ),
            "example_fix": 'location = "eastus"',
        }

    if rule_id == "FINOPS_SKU_001":
        return {
            "rule_id": rule_id,
            "severity": finding.get("severity", "high"),
            "summary": "Blocked expensive SKU detected.",
            "explanation": (
                "This SKU is blocked because it may create unnecessary cloud spend "
                "for the current environment."
            ),
            "terraform_fix": (
                "Replace the blocked SKU with a lower-cost approved SKU, or document "
                "a business exception."
            ),
            "example_fix": 'size = "Standard_B1s"',
        }

    return {
        "rule_id": rule_id,
        "severity": finding.get("severity", "unknown"),
        "summary": "FinOps issue detected.",
        "explanation": "Review this finding and compare it with the FinOps policy.",
        "terraform_fix": "Update Terraform to satisfy the policy rule.",
        "example_fix": None,
    }


def main():
    if not FINDINGS_FILE.exists():
        print("No findings file found. Run finops_scan.py first.")
        return 1

    findings = json.loads(FINDINGS_FILE.read_text(encoding="utf-8"))
    recommendations = [recommendation_for_finding(finding) for finding in findings]

    RECOMMENDATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RECOMMENDATIONS_FILE.write_text(
        json.dumps(recommendations, indent=2),
        encoding="utf-8",
    )

    print(f"Generated {len(recommendations)} AI-style recommendations.")
    print(f"Output: {RECOMMENDATIONS_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())