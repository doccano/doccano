import ApiService from '@/services/api.service'

class MemberService {
  constructor() {
    this.request = new ApiService()
  }

  getMemberList(projectId) {
    return this.request.get(`/projects/${projectId}/users`)
  }

  addMember(projectId, userId, role) {
    const data = {
      id: userId,
      role
    }
    return this.request.post(`/projects/${projectId}/users`, data)
  }

  deleteMember(projectId, userId) {
    return this.request.delete(`/projects/${projectId}/users/${userId}`)
  }

  updateMemberRole(projectId, userId, role) {
    const data = {
      role
    }
    return this.request.patch(`/projects/${projectId}/users/${userId}`, data)
  }
}

export default new MemberService()
