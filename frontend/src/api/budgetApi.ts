const API_BASE_URL = "http://127.0.0.1:8000";

export interface FixRecommendation {
  vuln_id: number;
  cve_id: string;
  asset_id: number;
  asset_name: string;
  asset_type: string;
  criticality: string;
  exposure: string;
  patch_status: string;
  cvss_score: number;
  current_risk_score: number;
  estimated_cost: number;
  risk_reduction: number;
  priority_ratio: number;
}

export interface BudgetOptimizationResponse {
  selected_fixes: FixRecommendation[];
  total_cost: number;
  total_risk_reduction: number;
  remaining_budget: number;
  skipped_fixes: FixRecommendation[];
  total_budget: number;
}

export async function fetchBudgetOptimization(totalBudget: number): Promise<BudgetOptimizationResponse> {
  const response = await fetch(`${API_BASE_URL}/budget/optimize?total_budget=${totalBudget}`);
  if (!response.ok) {
    throw new Error("Failed to fetch budget optimization");
  }
  return response.json();
}