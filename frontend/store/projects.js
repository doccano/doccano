export const state = () => ({
  current: {}
})

export const getters = {
  currentProject(state) {
    return state.current
  },
  getCurrentUserRole(state) {
    return state.current.current_users_role || {}
  },
  canViewApproveButton(state) {
    const role = state.current.current_users_role
    return role && !role.is_annotator
  },
  getLink(state) {
    return state.current.pageLink
  }
}

export const mutations = {
  setCurrent(state, payload) {
    state.current = payload
  }
}

export const actions = {
  async setCurrentProject({ commit }, projectId) {
    try {
      const response = await this.$services.project.findById(projectId)
      commit('setCurrent', response)
    } catch (error) {
      throw new Error(error)
    }
  }
}
