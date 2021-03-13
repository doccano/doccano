import ProjectService from '@/services/project.service'

export const state = () => ({
  current: {},
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
    if (state.current.project_type === 'DocumentClassification') {
      return 'text-classification'
    } else if (state.current.project_type === 'SequenceLabeling') {
      return 'sequence-labeling'
    } else if (state.current.project_type === 'Seq2seq') {
      return 'sequence-to-sequence'
    } else {
      return ''
    }
  },
}

export const mutations = {
  setCurrent(state, payload) {
    state.current = payload
  }
}

export const actions = {
  setCurrentProject({ commit }, projectId) {
    return ProjectService.fetchProjectById(projectId)
      .then((response) => {
        commit('setCurrent', response.data)
      })
      .catch((error) => {
        throw new Error(error)
      })
  }
}
