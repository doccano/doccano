import DocumentService from '@/services/document.service'

export const state = () => ({
  items: [],
  selected: [],
  loading: false
})

export const getters = {
  isDocumentSelected(state) {
    return state.selected.length > 0
  }
}

export const mutations = {
  setDocumentList(state, payload) {
    state.items = payload
  },
  addDocument(state, document) {
    state.items.unshift(document)
  },
  deleteDocument(state, documentId) {
    state.items = state.items.filter(item => item.id !== documentId)
  },
  updateSelected(state, selected) {
    state.selected = selected
  },
  updateDocument(state, document) {
    const item = state.items.find(item => item.id === document.id)
    Object.assign(item, document)
  },
  resetSelected(state) {
    state.selected = []
  },
  setLoading(state, payload) {
    state.loading = payload
  }
}

export const actions = {
  getDocumentList({ commit }, config) {
    commit('setLoading', true)
    return DocumentService.getDocumentList()
      .then((response) => {
        commit('setDocumentList', response)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  createDocument({ commit }, data) {
    DocumentService.addDocument(data.projectId, data)
      .then((response) => {
        commit('addDocument', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateDocument({ commit }, data) {
    DocumentService.updateDocument(data.projectId, data.id, data)
      .then((response) => {
        commit('updateDocument', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteDocument({ commit, state }, projectId) {
    for (const document of state.selected) {
      DocumentService.deleteDocument(projectId, document.id)
        .then((response) => {
          commit('deleteDocument', document.id)
        })
        .catch((error) => {
          alert(error)
        })
    }
    commit('resetSelected')
  }
}
