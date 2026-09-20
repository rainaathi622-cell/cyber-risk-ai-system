import { useState, useEffect } from 'react'
import { fetchRiskSummaries } from '../api/riskApi'
import type { AssetRiskSummary } from '../api/riskApi'

function Assets() {
  const [assets, setAssets] = useState<AssetRiskSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState<string>('')

  useEffect(() => {
    setLoading(true)
    fetchRiskSummaries(filter || undefined)
      .then((data) => {
        setAssets(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [filter])

  const riskColor = (risk: string) => {
    if (risk === 'Critical') return 'bg-red-100 text-red-700'
    if (risk === 'High') return 'bg-orange-100 text-orange-700'
    if (risk === 'Medium') return 'bg-yellow-100 text-yellow-700'
    return 'bg-green-100 text-green-700'
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="flex justify-between items-center mb-6">
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

      {loading && <p className="text-gray-600">Loading assets...</p>}
      {error && <p className="text-red-600">Error: {error}</p>}

      {!loading && !error && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
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
            <p className="text-center text-gray-500 py-8">No assets found for this filter.</p>
          )}
        </div>
      )}
    </div>
  )
}

export default Assets