import ApiService from '@/services/api.service'

class RoleService {
  constructor() {
    this.request = ApiService
  }

  getRoleList() {
    return this.request.get('/roles')
  }
}

export default new RoleService()
