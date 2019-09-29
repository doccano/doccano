const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

class TokenService {
  getToken() {
    return localStorage.getItem(TOKEN_KEY)
  }

  saveToken(accessToken) {
    localStorage.setItem(TOKEN_KEY, accessToken)
  }

  removeToken() {
    localStorage.removeItem(TOKEN_KEY)
  }

  getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
  }

  saveRefreshToken(refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
  }

  removeRefreshToken() {
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  }
}

export default new TokenService()
