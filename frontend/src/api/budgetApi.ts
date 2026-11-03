import { authFetch } from './http'

export interface FixRecommendation {
  vuln_id: number
  cve_id: string
  asset_id: number
  asset_name: string
  asset_type: string
  criticality: string
  exposure: string
  patch_status: string
  cvss_score: number
  current_risk_score: number
  estimated_cost: number
  risk_reduction: number
  priority_ratio: number
}

export interface BudgetOptimizationResponse {
  selected_fixes: FixRecommendation[]
  total_cost: number
  total_risk_reduction: number
  remaining_budget: number
  skipped_fixes: FixRecommendation[]
  total_budget: number
}

export async function fetchBudgetOptimization(totalBudget: number): Promise<BudgetOptimizationResponse> {
  const response = await authFetch(`/budget/optimize?total_budget=${totalBudget}`)

  if (response.status === 422) {
    throw new Error('Budget must be more than ₹0 and at most ₹10,00,00,000')
  }
  if (!response.ok) {
    throw new Error('Could not get recommendations right now. Please try again.')
  }
  return response.json()
}