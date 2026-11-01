import { useState, useEffect, useCallback } from 'react'
import { fetchRiskSummaries } from '../api/riskApi'
import type { AssetRiskSummary } from '../api/riskApi'
import ErrorBox from '../components/ErrorBox'

function Assets() {
  const [assets, setAssets] = useState<AssetRiskSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState<string>('')

  const loadAssets = useCallback(() => {
    setLoading(true)
    setError(null)
    fetchRiskSummaries(filter || undefined)
      .then((data) => setAssets(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [filter])

  useEffect(() => {
    loadAssets()
  }, [loadAssets])

  const riskColor = (risk: string) => {
    if (risk === 'Critical') return 'bg-red-100 text-red-700'
    if (risk === 'High') return 'bg-orange-100 text-orange-700'
    if (risk === 'Medium') return 'bg-yellow-100 text-yellow-700'
    return 'bg-green-100 text-green-700'
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-8">
      <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Asset Inventory</h1>

        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="border border-gray-300 rounded-md px-3 py-2 bg-white"
        >
          <option value="">All Risk Levels</option>
          <option value="Critical">Critical</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>

      {loading && (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-3"></div>
          <p className="text-gray-600">Loading assets...</p>
        </div>
      )}

      {error && <ErrorBox message={error} onRetry={loadAssets} />}

      {!loading && !error && (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Asset Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Criticality</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Exposure</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vulns</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {assets.map((asset) => (
                <tr key={asset.asset_id}>
                  <td className="px-6 py-4 text-sm text-gray-900 font-medium">{asset.asset_name}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{asset.asset_type}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{asset.criticality}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{asset.exposure}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{asset.vulnerability_count}</td>
                  <td className="px-6 py-4 text-sm text-gray-900 font-semibold">{asset.calculated_score.toFixed(1)}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${riskColor(asset.risk_level)}`}>
                      {asset.risk_level}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {assets.length === 0 && (
            <p className="text-center text-gray-500 py-8">
              {filter
                ? `No assets with risk level "${filter}".`
                : 'No assets have been added yet.'}
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default Assets