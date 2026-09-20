import { useState } from 'react'
import { fetchBudgetOptimization } from '../api/budgetApi'
import type { BudgetOptimizationResponse } from '../api/budgetApi'

function Budget() {
  const [budgetInput, setBudgetInput] = useState('50000')
  const [result, setResult] = useState<BudgetOptimizationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hasSearched, setHasSearched] = useState(false)

  const handleOptimize = () => {
    const budgetValue = parseFloat(budgetInput)

    if (isNaN(budgetValue) || budgetValue <= 0) {
      setError('Please enter a valid budget amount greater than 0')
      return
    }

    setLoading(true)
    setError(null)
    setHasSearched(true)

    fetchBudgetOptimization(budgetValue)
      .then((data) => {
        setResult(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }

  const riskColor = (risk_score: number) => {
    if (risk_score >= 70) return 'bg-red-100 text-red-700'
    if (risk_score >= 50) return 'bg-orange-100 text-orange-700'
    if (risk_score >= 30) return 'bg-yellow-100 text-yellow-700'
    return 'bg-green-100 text-green-700'
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">Budget Recommendation</h1>
      <p className="text-gray-600 mb-6">
        Enter your available security budget to see which fixes give you the most risk reduction for your money.
      </p>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Total Available Budget (₹)
        </label>
        <div className="flex gap-3">
          <input
            type="number"
            value={budgetInput}
            onChange={(e) => setBudgetInput(e.target.value)}
            className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="e.g. 50000"
          />
          <button
            onClick={handleOptimize}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? 'Calculating...' : 'Get Recommendations'}
          </button>
        </div>
        {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
      </div>

      {hasSearched && result && !loading && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-lg shadow p-5">
              <h3 className="text-xs font-medium text-gray-500 uppercase">Total Budget</h3>
              <p className="text-2xl font-bold text-gray-800 mt-1">₹{result.total_budget.toLocaleString()}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-5">
              <h3 className="text-xs font-medium text-gray-500 uppercase">Amount Used</h3>
              <p className="text-2xl font-bold text-blue-600 mt-1">₹{result.total_cost.toLocaleString()}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-5">
              <h3 className="text-xs font-medium text-gray-500 uppercase">Risk Reduction</h3>
              <p className="text-2xl font-bold text-green-600 mt-1">{result.total_risk_reduction.toFixed(1)} pts</p>
            </div>
            <div className="bg-white rounded-lg shadow p-5">
              <h3 className="text-xs font-medium text-gray-500 uppercase">Remaining Budget</h3>
              <p className="text-2xl font-bold text-gray-800 mt-1">₹{result.remaining_budget.toLocaleString()}</p>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden mb-6">
            <div className="px-6 py-4 border-b border-gray-200 bg-green-50">
              <h2 className="text-lg font-semibold text-gray-800">
                ✅ Recommended Fixes ({result.selected_fixes.length})
              </h2>
              <p className="text-sm text-gray-600">These fit within your budget, prioritized by best value</p>
            </div>
            {result.selected_fixes.length === 0 ? (
              <p className="text-center text-gray-500 py-8">No fixes fit within this budget. Try a higher amount.</p>
            ) : (
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Asset</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">CVE</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Current Risk</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cost</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk Reduction</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {result.selected_fixes.map((fix) => (
                    <tr key={fix.vuln_id}>
                      <td className="px-6 py-4 text-sm text-gray-900 font-medium">{fix.asset_name}</td>
                      <td className="px-6 py-4 text-sm text-gray-500 font-mono">{fix.cve_id}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${riskColor(fix.current_risk_score)}`}>
                          {fix.current_risk_score}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">₹{fix.estimated_cost.toLocaleString()}</td>
                      <td className="px-6 py-4 text-sm text-green-600 font-semibold">-{fix.risk_reduction}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {result.skipped_fixes.length > 0 && (
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
                <h2 className="text-lg font-semibold text-gray-800">
                  ⏳ Not Included ({result.skipped_fixes.length})
                </h2>
                <p className="text-sm text-gray-600">These didn't fit in your budget — consider for next cycle</p>
              </div>
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Asset</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">CVE</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cost</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Would Reduce Risk By</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {result.skipped_fixes.slice(0, 5).map((fix) => (
                    <tr key={fix.vuln_id}>
                      <td className="px-6 py-4 text-sm text-gray-900">{fix.asset_name}</td>
                      <td className="px-6 py-4 text-sm text-gray-500 font-mono">{fix.cve_id}</td>
                      <td className="px-6 py-4 text-sm text-gray-500">₹{fix.estimated_cost.toLocaleString()}</td>
                      <td className="px-6 py-4 text-sm text-gray-500">{fix.risk_reduction}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default Budget