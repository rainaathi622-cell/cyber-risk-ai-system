import { Link, useLocation, useNavigate } from 'react-router-dom'

function Nav() {
  const location = useLocation()
  const navigate = useNavigate()
  const isLoggedIn = !!localStorage.getItem('access_token')

  const linkClass = (path: string) =>
    location.pathname === path
      ? 'text-blue-300 font-semibold'
      : 'hover:text-blue-300'

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    navigate('/login')
  }

  return (
    <nav className="bg-gray-800 text-white px-6 py-4 flex gap-6 items-center justify-between">
      <div className="flex gap-6">
        <Link to="/" className={linkClass('/')}>Dashboard</Link>
        <Link to="/assets" className={linkClass('/assets')}>Assets</Link>
        <Link to="/budget" className={linkClass('/budget')}>Budget</Link>
        {!isLoggedIn && <Link to="/login" className={linkClass('/login')}>Login</Link>}
      </div>
      {isLoggedIn && (
        <button onClick={handleLogout} className="text-sm hover:text-red-300">
          Logout
        </button>
      )}
    </nav>
  )
}

export default Nav