import ProjectService from '@/services/project.service'

export const state = () => ({
  projects: [],
  selected: [],
  current: null,
  loading: false
})

export const getters = {
  isProjectSelected(state) {
    return state.selected.length > 0
  },
  currentProject(state) {
    return state.current
  },
  headers() {
    return [
      {
        text: 'Name',
        align: 'left',
        value: 'name'
      },
      {
        text: 'Description',
        value: 'description'
      },
      {
        text: 'Type',
        value: 'project_type'
      }
    ]
  }
}

export const mutations = {
  setProjectList(state, payload) {
    state.projects = payload
  },
  createProject(state, project) {
    state.projects.unshift(project)
  },
  updateProject(state, project) {
    const item = state.projects.find(item => item.id === project.id)
    Object.assign(item, project)
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
  },
  setCurrent(state, payload) {
    state.current = payload
  }
}

export const actions = {
  getProjectList({ commit }, config) {
    commit('setLoading', true)
    ProjectService.getProjectList()
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
  updateProject({ commit }, data) {
    ProjectService.updateProject(data.projectId, data)
      .then((response) => {
        commit('updateProject', response)
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
  },
  setCurrentProject({ commit }, projectId) {
    return ProjectService.fetchProjectById(projectId)
      .then((response) => {
        commit('setCurrent', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateCurrentProject({ commit }, data) {
    ProjectService.updateProject(data.projectId, data)
      .then((response) => {
        commit('setCurrent', response)
      })
      .catch((error) => {
        alert(error)
      })
  }
}
