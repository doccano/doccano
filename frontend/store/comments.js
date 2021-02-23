import CommentService from '@/services/comment.service'
import UserService from '@/services/user.service'

export const state = () => ({
  comments: [],
  selectedComments: [],
  totalComments: 0,
  userId: -1,
  loading: false
})

export const getters = {
  isCommentSelected(state) {
    return state.selectedComments.length > 0
  }
}
export const mutations = {
  setCommentList(state, payload) {
    state.comments = payload
  },
  addComment(state, payload) {
    state.comments.unshift(payload)
  },
  updateComment(state, payload) {
    const item = state.comments.find(item => item.id === payload.id)
    Object.assign(item, payload)
  },
  deleteComment(state, commentId) {
    state.comments = state.comments.filter(item => item.id !== commentId)
  },
  updateSelectedComments(state, selected) {
    state.selectedComments = selected
  },
  resetSelectedComments(state) {
    state.selectedComments = []
  },
  setTotalComments(state, payload) {
    state.totalComments = payload
  },
  setUserId(state, payload) {
    state.userId = payload.id
  },
  setLoading(state, payload) {
    state.loading = payload
  }
}

export const actions = {
  getCommentList({ commit, state }, payload) {
    commit('setLoading', true)
    return CommentService.getCommentList(payload.projectId, payload.docId)
      .then((response) => {
        commit('setCommentList', response.data)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  getProjectCommentList({ commit, state }, payload) {
    commit('setLoading', true)
    return CommentService.getProjectCommentList(payload.projectId)
      .then((response) => {
        commit('setCommentList', response.data)
        commit('setTotalComments', response.data.count)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  addComment({ commit, state }, payload) {
    CommentService.addComment(payload.projectId, payload.docId, payload)
      .then((response) => {
        commit('addComment', response.data)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateComment({ commit, state }, payload) {
    CommentService.updateComment(payload.projectId, payload.docId, payload.commentId, payload)
      .then((response) => {
        commit('updateComment', response.data)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteComment({ commit, state }, payload) {
    for (const comment of state.selectedComments) {
      CommentService.deleteComment(payload.projectId, comment.document, comment.id)
        .then((response) => {
          commit('deleteComment', comment.id)
        })
        .catch((error) => {
          alert(error)
        })
      commit('resetSelectedComments')
    }
  },
  getMyUserId({ commit, state }) {
    UserService.getMe()
      .then((response) => {
        commit('setUserId', response.data)
      })
      .catch((error) => {
        alert(error)
      })
  }
}
