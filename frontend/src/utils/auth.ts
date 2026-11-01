const TOKEN_KEY = 'access_token'

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}

// A token counts as valid only if it exists, can be read, and has not expired
export function isTokenValid(): boolean {
  const token = localStorage.getItem(TOKEN_KEY)
  if (!token) return false

  try {
    const payloadPart = token.split('.')[1]
    const base64 = payloadPart.replace(/-/g, '+').replace(/_/g, '/')
    const payload = JSON.parse(atob(base64))

    if (!payload.exp) return true
    return payload.exp * 1000 > Date.now()
  } catch {
    return false
  }
}