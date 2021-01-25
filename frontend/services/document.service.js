import ApiService from '@/services/api.service'

class DocumentService {
  constructor() {
    this.request = ApiService
  }

  getDocumentList({ projectId, limit = 10, offset = 0, q = '', isChecked = '', filterName = '' }) {
    return this.request.get(`/projects/${projectId}/docs?limit=${limit}&offset=${offset}&q=${q}&${filterName}=${isChecked}`)
  }

  addDocument(projectId, payload) {
    return this.request.post(`/projects/${projectId}/docs`, payload)
  }

  deleteAllDocuments(projectId) {
    return this.request.delete(`/projects/${projectId}/docs`)
  }

  deleteDocument(projectId, docId) {
    return this.request.delete(`/projects/${projectId}/docs/${docId}`)
  }

  updateDocument(projectId, docId, payload) {
    return this.request.patch(`/projects/${projectId}/docs/${docId}`, payload)
  }

  uploadFile(projectId, payload, config = {}) {
    return this.request.post(`/projects/${projectId}/docs/upload`, payload, config)
  }

  exportFile(projectId, format, onlyApproved) {
    const headers = {}
    if (format === 'csv') {
      headers.Accept = 'text/csv; charset=utf-8'
      headers['Content-Type'] = 'text/csv; charset=utf-8'
    } else if (format === 'txt') {
      headers.Accept = 'text/plain; charset=utf-8'
      headers['Content-Type'] = 'text/plain; charset=utf-8'
    } else {
      headers.Accept = 'application/json'
      headers['Content-Type'] = 'application/json'
    }
    const config = {
      responseType: 'blob',
      params: {
        q: format,
        onlyApproved
      },
      headers
    }
    return this.request.get(`/projects/${projectId}/docs/download`, config)
  }

  approveDocument(projectId, docId, payload) {
    return this.request.post(`/projects/${projectId}/docs/${docId}/approve-labels`, payload)
  }
}

export default new DocumentService()
