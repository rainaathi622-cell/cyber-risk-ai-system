function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">
        Security Risk Dashboard
      </h1>
      <p className="text-gray-600">
        Overview of your organization's cybersecurity risk will appear here.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Overall Risk Score</h2>
          <p className="text-3xl font-bold text-red-600 mt-2">Coming Soon</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Critical Vulnerabilities</h2>
          <p className="text-3xl font-bold text-orange-500 mt-2">Coming Soon</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-sm font-medium text-gray-500">Budget Recommended</h2>
          <p className="text-3xl font-bold text-green-600 mt-2">Coming Soon</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard