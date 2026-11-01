import { Navigate } from 'react-router-dom'
import type { ReactNode } from 'react'
import { isTokenValid, clearToken } from '../utils/auth'

function ProtectedRoute({ children }: { children: ReactNode }) {
  if (!isTokenValid()) {
    clearToken()
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

export default ProtectedRoute