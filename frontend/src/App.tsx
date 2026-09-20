import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Assets from './pages/Assets'
import Budget from './pages/Budget'

function App() {
  return (
    <BrowserRouter>
      <nav className="bg-gray-800 text-white px-6 py-4 flex gap-6">
        <Link to="/" className="hover:text-blue-300">Dashboard</Link>
        <Link to="/assets" className="hover:text-blue-300">Assets</Link>
        <Link to="/budget" className="hover:text-blue-300">Budget</Link>
        <Link to="/login" className="hover:text-blue-300">Login</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/assets" element={<Assets />} />
        <Route path="/budget" element={<Budget />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App