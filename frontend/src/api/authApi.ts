import { API_BASE_URL } from './http'

export interface LoginResponse {
  access_token: string
  token_type: string
}

async function readError(response: Response, fallback: string): Promise<string> {
  const errorData = await response.json().catch(() => ({}))
  return typeof errorData.detail === 'string' ? errorData.detail : fallback
}

export async function loginUser(email: string, password: string): Promise<LoginResponse> {
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
  } catch {
    throw new Error('Cannot reach the server. If it was idle, wait one minute and try again.')
  }

  if (!response.ok) {
    throw new Error(await readError(response, 'Login failed'))
  }
  return response.json()
}

export async function signupUser(email: string, password: string, fullName: string): Promise<void> {
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name: fullName }),
    })
  } catch {
    throw new Error('Cannot reach the server. If it was idle, wait one minute and try again.')
  }

  if (!response.ok) {
    throw new Error(await readError(response, 'Signup failed'))
  }
}