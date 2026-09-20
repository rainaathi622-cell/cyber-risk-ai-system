import { useState, useEffect } from 'react'
import { fetchRiskStats } from '../api/riskApi'
import type { RiskStats } from '../api/riskApi'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

function Dashboard() {
  const [stats, setStats] = useState<RiskStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchRiskStats()
      .then((data) => {
        setStats(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 p-8">
        <p className="text-gray-600">Loading dashboard data...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 p-8">
        <p className="text-red-600">Error loading data: {error}</p>
        <p className="text-gray-500 text-sm mt-2">Make sure your backend server is running at http://127.0.0.1:8000</p>
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
    { name: 'Critical', count: stats?.critical_count || 0 },
    { name: 'High', count: stats?.high_count || 0 },
    { name: 'Medium', count: stats?.medium_count || 0 },
    { name: 'Low', count: stats?.low_count || 0 },
  ]

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">
        Security Risk Dashboard
      </h1>
      <p className="text-gray-600 mb-6">
        Overview of your organization's cybersecurity risk.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Overall Risk Score</h2>
          <p className={`text-3xl font-bold mt-2 ${getScoreColor(stats?.overall_score || 0)}`}>
            {stats?.overall_score}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Critical Assets</h2>
          <p className="text-3xl font-bold text-red-600 mt-2">
            {stats?.critical_count}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Total Assets Monitored</h2>
          <p className="text-3xl font-bold text-blue-600 mt-2">
            {stats?.total_assets}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Risk Level Distribution</h2>
        <div className="space-y-3">
          <RiskBar label="Critical" count={stats?.critical_count || 0} total={stats?.total_assets || 1} color="bg-red-500" />
          <RiskBar label="High" count={stats?.high_count || 0} total={stats?.total_assets || 1} color="bg-orange-500" />
          <RiskBar label="Medium" count={stats?.medium_count || 0} total={stats?.total_assets || 1} color="bg-yellow-500" />
          <RiskBar label="Low" count={stats?.low_count || 0} total={stats?.total_assets || 1} color="bg-green-500" />
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