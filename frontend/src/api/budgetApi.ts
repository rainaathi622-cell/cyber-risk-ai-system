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

async function fetchWithRetry(url: string, retries = 1, delayMs = 800): Promise<Response> {
  try {
    const response = await fetch(url);
    if (!response.ok && retries > 0) {
      await new Promise((resolve) => setTimeout(resolve, delayMs));
      return fetchWithRetry(url, retries - 1, delayMs);
    }
    return response;
  } catch (err) {
    if (retries > 0) {
      await new Promise((resolve) => setTimeout(resolve, delayMs));
      return fetchWithRetry(url, retries - 1, delayMs);
    }
    throw err;
  }
}

export async function fetchBudgetOptimization(totalBudget: number): Promise<BudgetOptimizationResponse> {
  const response = await fetchWithRetry(`${API_BASE_URL}/budget/optimize?total_budget=${totalBudget}`);
  if (!response.ok) {
    throw new Error("Failed to fetch budget optimization");
  }
  return response.json();
}