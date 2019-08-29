import ProjectService from '@/services/project.service'

export default {
  namespaced: true,

  state: () => ({
    projects: [],
    selected: []
  }),

  mutations: {
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
    }
  },

  actions: {
    getProjectList(context, config) {
      return ProjectService.getProjectList()
        .then((response) => {
          context.commit('setProjectList', response)
        })
        .catch((error) => {
          alert(error)
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
}
