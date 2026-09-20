import { Link, useLocation } from 'react-router-dom'

function Nav() {
  const location = useLocation()

  const linkClass = (path: string) =>
    location.pathname === path
      ? 'text-blue-300 font-semibold'
      : 'hover:text-blue-300'

  return (
    <nav className="bg-gray-800 text-white px-6 py-4 flex gap-6">
      <Link to="/" className={linkClass('/')}>Dashboard</Link>
      <Link to="/assets" className={linkClass('/assets')}>Assets</Link>
      <Link to="/budget" className={linkClass('/budget')}>Budget</Link>
      <Link to="/login" className={linkClass('/login')}>Login</Link>
    </nav>
  )
}

export default Nav