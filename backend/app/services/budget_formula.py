# Base cost assumptions (in rupees) - these are estimates for MVP purposes

BASE_FIX_COST = 5000

ASSET_TYPE_COST_MULTIPLIER = {
    "Server": 2.0,
    "Database": 2.5,
    "Cloud Instance": 1.8,
    "Application": 1.5,
    "Laptop": 0.8
}

CRITICALITY_COST_MULTIPLIER = {
    "Critical": 2.0,
    "High": 1.5,
    "Medium": 1.2,
    "Low": 1.0
}


def estimate_fix_cost(asset_type: str, criticality: str) -> float:
    """
    Estimate the cost to fix a vulnerability on a given asset.
    """
    type_multiplier = ASSET_TYPE_COST_MULTIPLIER.get(asset_type, 1.5)
    criticality_multiplier = CRITICALITY_COST_MULTIPLIER.get(criticality, 1.2)

    cost = BASE_FIX_COST * type_multiplier * criticality_multiplier
    return round(cost, 2)


def calculate_risk_reduction_value(current_risk_score: float, cvss_score: float, criticality: str, exposure: str, patch_status: str) -> float:
    """
    Estimate how much the risk score would drop if this specific vulnerability is fixed.
    We simulate this by recalculating the score as if patch_status became 'Up-to-date'.
    """
    from services.risk_formula import calculate_risk_score

    score_if_fixed = calculate_risk_score(cvss_score, criticality, exposure, "Up-to-date")
    risk_reduction = current_risk_score - score_if_fixed

    return max(round(risk_reduction, 2), 0)


def build_fix_recommendations(vulnerabilities_with_context: list) -> list:
    """
    For each vulnerability, calculate cost and risk reduction value,
    then compute a priority ratio (risk_reduction / cost).

    vulnerabilities_with_context: list of dicts, each containing:
        - vuln_id, cve_id, asset_id, asset_name, asset_type,
          criticality, exposure, patch_status, cvss_score, current_risk_score

    Returns the same list enriched with cost, risk_reduction, and priority_ratio,
    sorted by priority_ratio descending (best value first).
    """
    recommendations = []

    for vuln in vulnerabilities_with_context:
        cost = estimate_fix_cost(vuln["asset_type"], vuln["criticality"])
        risk_reduction = calculate_risk_reduction_value(
            vuln["current_risk_score"],
            vuln["cvss_score"],
            vuln["criticality"],
            vuln["exposure"],
            vuln["patch_status"]
        )

        priority_ratio = round(risk_reduction / cost, 6) if cost > 0 else 0

        recommendations.append({
            **vuln,
            "estimated_cost": cost,
            "risk_reduction": risk_reduction,
            "priority_ratio": priority_ratio
        })

    recommendations.sort(key=lambda x: x["priority_ratio"], reverse=True)
    return recommendations


def optimize_budget_allocation(recommendations: list, total_budget: float) -> dict:
    """
    Greedy algorithm: pick fixes in priority order until budget runs out.

    Returns a dict with:
        - selected_fixes: list of fixes we can afford, in priority order
        - total_cost: sum of selected fix costs
        - total_risk_reduction: sum of risk reduction achieved
        - remaining_budget: leftover money
        - skipped_fixes: fixes that didn't fit in the budget
    """
    selected_fixes = []
    skipped_fixes = []
    remaining_budget = total_budget
    total_risk_reduction = 0

    for fix in recommendations:
        if fix["estimated_cost"] <= remaining_budget:
            selected_fixes.append(fix)
            remaining_budget -= fix["estimated_cost"]
            total_risk_reduction += fix["risk_reduction"]
        else:
            skipped_fixes.append(fix)

    total_cost = total_budget - remaining_budget

    return {
        "selected_fixes": selected_fixes,
        "total_cost": round(total_cost, 2),
        "total_risk_reduction": round(total_risk_reduction, 2),
        "remaining_budget": round(remaining_budget, 2),
        "skipped_fixes": skipped_fixes,
        "total_budget": total_budget
    }