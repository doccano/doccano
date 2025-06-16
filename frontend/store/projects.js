export const state = () => ({
  current: {},
  currentMember: null
})

export const getters = {
  currentProject(state) {
    return state.current
  },

  project(state) {
    return state.current
  },

  isProjectAdmin(state) {
    return state.currentMember?.isProjectAdmin || false
  },

  currentMember(state) {
    return state.currentMember
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
  },
  setCurrentMember(state, member) {
    state.currentMember = member
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
  },

  async setCurrentMember({ commit }, { projectId, $repositories }) {
    try {
      const member = await $repositories.member.fetchMyRole(projectId)
      commit('setCurrentMember', member)
    } catch (error) {
      console.error('Failed to set current member:', error)
    }
  }
}
