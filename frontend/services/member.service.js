import ApiService from '@/services/api.service'

class MemberService {
  constructor() {
    this.request = ApiService
  }

  getMemberList(projectId) {
    return this.request.get(`/projects/${projectId}/roles`)
  }

  addMember(projectId, user, role) {
    const data = {
      user,
      role
    }
    return this.request.post(`/projects/${projectId}/roles`, data)
  }

  deleteMember(projectId, userId) {
    return this.request.delete(`/projects/${projectId}/roles/${userId}`)
  }

  updateMemberRole(projectId, mappingId, role) {
    const data = {
      role
    }
    return this.request.patch(`/projects/${projectId}/roles/${mappingId}`, data)
  }
}

export default new MemberService()
