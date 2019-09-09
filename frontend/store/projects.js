import ProjectService from '@/services/project.service'

export const state = () => ({
  projects: [],
  selected: [],
  loading: false
})

export const getters = {
  isProjectSelected(state) {
    return state.selected.length > 0
  }
}

export const mutations = {
  setProjectList(state, payload) {
    state.projects = payload
  },
  createProject(state, project) {
    state.projects.unshift(project)
  },
  deleteProject(state, projectId) {
    state.projects = state.projects.filter(item => item.id !== projectId)
  },
  updateSelected(state, selected) {
    state.selected = selected
  },
  resetSelected(state) {
    state.selected = []
  },
  setLoading(state, payload) {
    state.loading = payload
  }
}

export const actions = {
  getProjectList({ commit }, config) {
    commit('setLoading', true)
    return ProjectService.getProjectList()
      .then((response) => {
        commit('setProjectList', response)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  createProject({ commit }, project) {
    ProjectService.createProject(project)
      .then((response) => {
        commit('createProject', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteProject({ commit, state }, config) {
    for (const project of state.selected) {
      ProjectService.deleteProject(project.id)
        .then((response) => {
          commit('deleteProject', project.id)
        })
        .catch((error) => {
          alert(error)
        })
    }
    commit('resetSelected')
  }
}
