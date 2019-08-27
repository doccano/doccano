import ApiService from '@/services/api.service'

class ProjectService {
  constructor() {
    this.request = new ApiService()
  }

  getProjectList() {
    return this.request.get('/projects')
  }

  createProject(data) {
    return this.request.post('/projects', data)
  }

  deleteProject(projectId) {
    return this.request.delete(`/projects/${projectId}`)
  }
}

export default new ProjectService()
