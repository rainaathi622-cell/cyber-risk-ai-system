function Assets() {
  const dummyAssets = [
    { id: 1, name: 'Web Server 01', type: 'Server', risk: 'High' },
    { id: 2, name: 'Employee Laptop 12', type: 'Laptop', risk: 'Medium' },
    { id: 3, name: 'Cloud DB Instance', type: 'Cloud', risk: 'Critical' },
  ]

  const riskColor = (risk: string) => {
    if (risk === 'Critical') return 'bg-red-100 text-red-700'
    if (risk === 'High') return 'bg-orange-100 text-orange-700'
    if (risk === 'Medium') return 'bg-yellow-100 text-yellow-700'
    return 'bg-green-100 text-green-700'
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Asset Inventory</h1>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Asset Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Risk Level
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {dummyAssets.map((asset) => (
              <tr key={asset.id}>
                <td className="px-6 py-4 text-sm text-gray-900">{asset.name}</td>
                <td className="px-6 py-4 text-sm text-gray-500">{asset.type}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${riskColor(asset.risk)}`}>
                    {asset.risk}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Assets
