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
    state.current = {
      ...payload,
      canDefineCategory: payload.canDefineCategory,
      canDefineLabel: payload.canDefineLabel,
      canDefineRelation: payload.canDefineRelation,
      canDefineSpan: payload.canDefineSpan
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
