export const state = () => ({
  current: {}
})

export const getters = {
  currentProject(state) {
    return state.current
  },

  project(state) {
    return state.current
  }
}

export const mutations = {
  setCurrent(state, payload) {
    state.current = payload
  },
  setPageTitle(state, title) {
    // Esta mutation pode ser usada para definir o título da página
    // Por enquanto, apenas armazenamos no estado atual
    if (state.current) {
      state.current.pageTitle = title
    }
  }
}

export const actions = {
  async setCurrentProject({ commit }, projectId) {
    try {
      const project = await this.$services.project.findById(projectId)
      commit('setCurrent', project)
    } catch (error) {
      throw new Error(error)
    }
  }
}
