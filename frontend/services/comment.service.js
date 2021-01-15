import ApiService from '@/services/api.service'

class CommentService {
  constructor() {
    this.request = ApiService
  }

  getCommentList({ projectId, docId }) {
    return this.request.get(`/projects/${projectId}/docs/${docId}/comments`)
  }

  addComment(projectId, docId, payload) {
    console.log(payload)
    return this.request.post(`/projects/${projectId}/docs/${docId}/comments`, payload)
  }

  deleteComment(projectId, docId, commentId) {
    return this.request.delete(`/projects/${projectId}/docs/${docId}/comments/${commentId}`)
  }

  updateComment(projectId, docId, commentId, payload) {
    return this.request.patch(`/projects/${projectId}/docs/${docId}/comments/${commentId}`, payload)
  }
}

export default new CommentService()
