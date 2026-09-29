const API_BASE_URL = "http://127.0.0.1:8000";

export interface RiskStats {
  overall_score: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  total_assets: number;
}

export interface AssetRiskSummary {
  asset_id: number;
  asset_name: string;
  asset_type: string;
  criticality: string;
  exposure: string;
  patch_status: string;
  calculated_score: number;
  risk_level: string;
  vulnerability_count: number;
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

export async function fetchRiskStats(): Promise<RiskStats> {
  const response = await fetchWithRetry(`${API_BASE_URL}/risk-scores/stats`);
  if (!response.ok) {
    throw new Error("Failed to fetch risk stats");
  }
  return response.json();
}

export async function fetchRiskSummaries(riskLevel?: string): Promise<AssetRiskSummary[]> {
  const url = riskLevel
    ? `${API_BASE_URL}/risk-scores/?risk_level=${riskLevel}`
    : `${API_BASE_URL}/risk-scores/`;

  const response = await fetchWithRetry(url);
  if (!response.ok) {
    throw new Error("Failed to fetch risk summaries");
  }
  return response.json();
}