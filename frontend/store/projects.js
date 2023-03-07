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
