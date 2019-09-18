import ApiService from '@/services/api.service'

class StatisticsService {
  constructor() {
    this.request = new ApiService()
  }

  getStatistics(projectId) {
    return this.request.get(`/projects/${projectId}/statistics`)
  }
}

export default new StatisticsService()
