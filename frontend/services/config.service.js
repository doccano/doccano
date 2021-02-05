import ApiService from '@/services/api.service'

class ConfigService {
  constructor() {
    this.request = ApiService
  }

  getConfigList({ projectId }) {
    return this.request.get(`/projects/${projectId}/auto-labeling-configs`)
  }

  addConfig(projectId, payload) {
    return this.request.post(`/projects/${projectId}/auto-labeling-configs`, payload)
  }

  deleteConfig(projectId, configId) {
    return this.request.delete(`/projects/${projectId}/auto-labeling-configs/${configId}`)
  }

  updateConfig(projectId, configId, payload) {
    return this.request.patch(`/projects/${projectId}/auto-labeling-configs/${configId}`, payload)
  }
}

export default new ConfigService()
