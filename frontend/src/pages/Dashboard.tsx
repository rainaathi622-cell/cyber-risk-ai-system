import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { fetchRiskStats } from '../api/riskApi'
import type { RiskStats } from '../api/riskApi'
import ErrorBox from '../components/ErrorBox'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

function Dashboard() {
  const [stats, setStats] = useState<RiskStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadStats = useCallback(() => {
    setLoading(true)
    setError(null)
    fetchRiskStats()
      .then((data) => setStats(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    loadStats()
  }, [loadStats])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 p-4 sm:p-8 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto mb-3"></div>
          <p className="text-gray-600">Loading dashboard data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 p-4 sm:p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Security Risk Dashboard</h1>
        <ErrorBox message={error} onRetry={loadStats} />
      </div>
    )
  }

  if (!stats || stats.total_assets === 0) {
    return (
      <div className="min-h-screen bg-gray-100 p-4 sm:p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Security Risk Dashboard</h1>
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <h2 className="text-lg font-semibold text-gray-800 mb-1">
            No assets are being monitored yet
          </h2>
          <p className="text-gray-600 mb-4">
            Add assets and their vulnerabilities. Risk scores will appear here automatically.
          </p>
          <Link
            to="/assets"
            className="bg-blue-600 text-white text-sm px-4 py-2 rounded-md hover:bg-blue-700 transition"
          >
            Go to Assets
          </Link>
        </div>
      </div>
    )
  }

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-red-600'
    if (score >= 50) return 'text-orange-500'
    if (score >= 30) return 'text-yellow-500'
    return 'text-green-600'
  }

  const chartData = [
    { name: 'Critical', count: stats.critical_count },
    { name: 'High', count: stats.high_count },
    { name: 'Medium', count: stats.medium_count },
    { name: 'Low', count: stats.low_count },
  ]

  const criticalCount = stats.critical_count

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">
        Security Risk Dashboard
      </h1>
      <p className="text-gray-600 mb-6">
        Overview of your organization's cybersecurity risk.
      </p>

      {criticalCount > 0 && (
        <div className="bg-red-50 border-l-4 border-red-500 rounded-md p-4 mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <p className="font-semibold text-red-800">
                {criticalCount} Critical Risk {criticalCount === 1 ? 'Asset' : 'Assets'} Detected
              </p>
              <p className="text-sm text-red-700">
                These assets need immediate attention. Review the Assets page for details.
              </p>
            </div>
          </div>
          <Link
            to="/assets"
            className="bg-red-600 text-white text-sm px-4 py-2 rounded-md hover:bg-red-700 transition whitespace-nowrap text-center"
          >
            View Critical Assets
          </Link>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Overall Risk Score</h2>
          <p className={`text-3xl font-bold mt-2 ${getScoreColor(stats.overall_score)}`}>
            {stats.overall_score}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Critical Assets</h2>
          <p className="text-3xl font-bold text-red-600 mt-2">
            {stats.critical_count}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Total Assets Monitored</h2>
          <p className="text-3xl font-bold text-blue-600 mt-2">
            {stats.total_assets}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Risk Level Distribution</h2>
        <div className="space-y-3">
          <RiskBar label="Critical" count={stats.critical_count} total={stats.total_assets} color="bg-red-500" />
          <RiskBar label="High" count={stats.high_count} total={stats.total_assets} color="bg-orange-500" />
          <RiskBar label="Medium" count={stats.medium_count} total={stats.total_assets} color="bg-yellow-500" />
          <RiskBar label="Low" count={stats.low_count} total={stats.total_assets} color="bg-green-500" />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6 mt-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Risk Distribution Chart</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count">
              <Cell fill="#dc2626" />
              <Cell fill="#f97316" />
              <Cell fill="#eab308" />
              <Cell fill="#16a34a" />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

function RiskBar({ label, count, total, color }: { label: string; count: number; total: number; color: string }) {
  const percentage = total > 0 ? (count / total) * 100 : 0

  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="font-medium text-gray-700">{label}</span>
        <span className="text-gray-500">{count} assets</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div className={`${color} h-3 rounded-full transition-all`} style={{ width: `${percentage}%` }}></div>
      </div>
    </div>
  )
}

export default Dashboard