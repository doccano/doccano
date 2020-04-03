import ApiService from '@/services/api.service'

class AuthService {
  constructor() {
    this.request = ApiService
  }

  postCredential(data) {
    this.request.removeHeader()
    return this.request.post('/auth-token', data)
  }
}

export default new AuthService()
