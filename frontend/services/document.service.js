import ApiService from '@/services/api.service'

class DocumentService {
  constructor() {
    this.request = new ApiService()
  }

  getDocumentList(projectId) {
    return this.request.get(`/projects/${projectId}/docs`)
  }

  addDocument(projectId, payload) {
    return this.request.post(`/projects/${projectId}/docs`, payload)
  }

  deleteDocument(projectId, docId) {
    return this.request.delete(`/projects/${projectId}/docs/${docId}`)
  }

  updateDocument(projectId, docId, payload) {
    return this.request.patch(`/projects/${projectId}/docs/${docId}`, payload)
  }

  uploadFile(projectId, payload) {
    return this.request.post(`/projects/${projectId}/docs/upload`, payload)
  }
}

export default new DocumentService()
