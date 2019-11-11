import ApiService from '@/services/api.service'

class UserService {
  constructor() {
    this.request = ApiService
  }

  getMe() {
    return this.request.get('/me')
  }

  getUserList(query) {
    return this.request.get(`/users?q=${query}`)
  }
}

export default new UserService()
