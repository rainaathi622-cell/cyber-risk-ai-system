import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from services.budget_formula import build_fix_recommendations, optimize_budget_allocation

# Sample vulnerabilities with context (simulating real data structure)
sample_vulns = [
    {
        "vuln_id": 1, "cve_id": "CVE-2024-0001", "asset_id": 1,
        "asset_name": "Web Server 01", "asset_type": "Server",
        "criticality": "Critical", "exposure": "Public", "patch_status": "Outdated",
        "cvss_score": 9.8, "current_risk_score": 98.0
    },
    {
        "vuln_id": 2, "cve_id": "CVE-2024-0002", "asset_id": 6,
        "asset_name": "Customer CRM Cloud Instance", "asset_type": "Cloud Instance",
        "criticality": "Critical", "exposure": "Public", "patch_status": "Outdated",
        "cvss_score": 8.5, "current_risk_score": 85.0
    },
    {
        "vuln_id": 3, "cve_id": "CVE-2024-0003", "asset_id": 7,
        "asset_name": "Employee Laptop - Finance01", "asset_type": "Laptop",
        "criticality": "Medium", "exposure": "Internal", "patch_status": "Outdated",
        "cvss_score": 6.0, "current_risk_score": 36.0
    },
    {
        "vuln_id": 4, "cve_id": "CVE-2024-0004", "asset_id": 5,
        "asset_name": "HR Database", "asset_type": "Database",
        "criticality": "Critical", "exposure": "Restricted", "patch_status": "Outdated",
        "cvss_score": 7.2, "current_risk_score": 43.2
    },
]

print("=== Building Recommendations ===")
recommendations = build_fix_recommendations(sample_vulns)
for r in recommendations:
    print(f"{r['asset_name']:<30} | Cost: ₹{r['estimated_cost']:>10} | Risk Reduction: {r['risk_reduction']:>6} | Priority: {r['priority_ratio']}")

print("\n=== Optimizing for Budget of ₹30,000 ===")
result = optimize_budget_allocation(recommendations, total_budget=30000)

print(f"\nSelected Fixes ({len(result['selected_fixes'])}):")
for fix in result["selected_fixes"]:
    print(f"  - {fix['asset_name']} (Cost: ₹{fix['estimated_cost']}, Risk Reduction: {fix['risk_reduction']})")

print(f"\nTotal Cost: ₹{result['total_cost']}")
print(f"Total Risk Reduction: {result['total_risk_reduction']}")
print(f"Remaining Budget: ₹{result['remaining_budget']}")
print(f"Skipped Fixes: {len(result['skipped_fixes'])}")