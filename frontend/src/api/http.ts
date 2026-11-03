// Day 34 (deployment) will change only this one line
export const API_BASE_URL = 'http://127.0.0.1:8000'

const TOKEN_KEY = 'access_token'

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

// Sends the login token with every request, retries once on server or network
// problems, and sends the user to the login page if the token is rejected.
export async function authFetch(path: string, retries = 1, delayMs = 800): Promise<Response> {
  const token = localStorage.getItem(TOKEN_KEY)

  let response: Response | null = null
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
  } catch {
    response = null
  }

  if (response === null) {
    if (retries > 0) {
      await sleep(delayMs)
      return authFetch(path, retries - 1, delayMs)
    }
    throw new Error('Cannot reach the server. Check that the backend is running.')
  }

  if (response.status === 401) {
    localStorage.removeItem(TOKEN_KEY)
    window.location.href = '/login'
    throw new Error('Your session has expired. Please log in again.')
  }

  if (response.status >= 500 && retries > 0) {
    await sleep(delayMs)
    return authFetch(path, retries - 1, delayMs)
  }

  return response
}