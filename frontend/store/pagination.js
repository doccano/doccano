export const state = () => ({
  limit: 10,
  page: 1,
  projectId: null
})

export const getters = {
  offset(state) {
    return Math.floor((state.page - 1) / state.limit) * state.limit
  },
  current(state) {
    return (state.page - 1) % state.limit
  },
  page(state) {
    return state.page
  },
  limit(state) {
    return state.limit
  }
}

export const mutations = {
  updatePage(state, page) {
    state.page = page
  },
  savePage(state) {
    const checkpoint = {}
    checkpoint[state.projectId] = state.page
    localStorage.setItem('checkpoint', JSON.stringify(checkpoint))
  },
  loadPage(state) {
    const checkpoint = JSON.parse(localStorage.getItem('checkpoint'))
    state.page = checkpoint[state.projectId] ? checkpoint[state.projectId] : 1
  },
  setProjectId(state, projectId) {
    state.projectId = projectId
  }
}

export const actions = {
  prevPage({ commit, state }) {
    const page = Math.max(state.page - 1, 1)
    commit('updatePage', page)
    commit('savePage')
  },
  nextPage({ commit, state }, total) {
    const page = Math.min(state.page + 1, total)
    commit('updatePage', page)
    commit('savePage')
  },
  initPage({ commit }, payload) {
    commit('setProjectId', payload.projectId)
    commit('loadPage')
  }
}
