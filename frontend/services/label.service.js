import ApiService from '@/services/api.service'

class LabelService {
  constructor() {
    this.request = ApiService
  }

  getLabelList(projectId) {
    return this.request.get(`/projects/${projectId}/labels`)
  }

  addLabel(projectId, payload) {
    return this.request.post(`/projects/${projectId}/labels`, payload)
  }

  deleteLabel(projectId, labelId) {
    return this.request.delete(`/projects/${projectId}/labels/${labelId}`)
  }

  updateLabel(projectId, labelId, payload) {
    return this.request.patch(`/projects/${projectId}/labels/${labelId}`, payload)
  }
}

export default new LabelService()
