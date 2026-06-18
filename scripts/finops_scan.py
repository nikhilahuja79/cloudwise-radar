from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY_FILE = ROOT / "policies" / "finops-rules.yaml"
TERRAFORM_DIR = ROOT / "infra" / "envs" / "dev"


def load_policy():
    if not POLICY_FILE.exists():
        raise FileNotFoundError(f"Missing policy file: {POLICY_FILE}")

    with POLICY_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def read_terraform_files():
    return {
        path: path.read_text(encoding="utf-8")
        for path in TERRAFORM_DIR.glob("*.tf")
    }


def check_required_tags(policy, terraform_text):
    findings = []
    required_tags = policy.get("required_tags", [])

    for tag in required_tags:
        if tag not in terraform_text:
            findings.append({
                "rule_id": "FINOPS_TAGS_001",
                "severity": "high",
                "message": f"Required tag '{tag}' was not found in Terraform files."
            })

    return findings


def check_allowed_locations(policy, terraform_text):
    findings = []
    allowed_locations = policy.get("allowed_locations", [])

    if "location" in terraform_text:
        has_allowed_location = any(location in terraform_text for location in allowed_locations)
        if not has_allowed_location:
            findings.append({
                "rule_id": "FINOPS_REGION_001",
                "severity": "medium",
                "message": "Terraform uses a location that is not in allowed_locations."
            })

    return findings


def check_blocked_skus(policy, terraform_text):
    findings = []
    blocked_skus = policy.get("blocked_skus", {})

    for category, skus in blocked_skus.items():
        for sku in skus:
            if sku in terraform_text:
                findings.append({
                    "rule_id": "FINOPS_SKU_001",
                    "severity": "high",
                    "message": f"Blocked SKU '{sku}' found in Terraform files.",
                    "category": category
                })

    return findings


def main():
    policy = load_policy()
    terraform_files = read_terraform_files()

    if not terraform_files:
        print("No Terraform files found.")
        return 1

    terraform_text = "\n".join(terraform_files.values())

    findings = []
    findings.extend(check_required_tags(policy, terraform_text))
    findings.extend(check_allowed_locations(policy, terraform_text))
    findings.extend(check_blocked_skus(policy, terraform_text))

    if findings:
        print("FinOps policy scan failed.\n")
        for finding in findings:
            print(f"[{finding['severity'].upper()}] {finding['rule_id']}: {finding['message']}")
        return 1

    print("FinOps policy scan passed. No violations found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())