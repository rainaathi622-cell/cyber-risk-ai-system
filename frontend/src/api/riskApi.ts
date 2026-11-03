import { authFetch } from './http'

export interface RiskStats {
  overall_score: number
  critical_count: number
  high_count: number
  medium_count: number
  low_count: number
  total_assets: number
}

export interface AssetRiskSummary {
  asset_id: number
  asset_name: string
  asset_type: string
  criticality: string
  exposure: string
  patch_status: string
  calculated_score: number
  risk_level: string
  vulnerability_count: number
}

export async function fetchRiskStats(): Promise<RiskStats> {
  const response = await authFetch('/risk-scores/stats')
  if (!response.ok) {
    throw new Error('Failed to load risk statistics')
  }
  return response.json()
}

export async function fetchRiskSummaries(riskLevel?: string): Promise<AssetRiskSummary[]> {
  const path = riskLevel
    ? `/risk-scores/?risk_level=${encodeURIComponent(riskLevel)}`
    : '/risk-scores/'

  const response = await authFetch(path)
  if (!response.ok) {
    throw new Error('Failed to load assets')
  }
  return response.json()
}