import LabelService from '@/services/label.service'

export const state = () => ({
  items: [],
  selected: [],
  loading: false
})

export const getters = {
  isLabelSelected(state) {
    return state.selected.length > 0
  }
}

export const mutations = {
  setLabelList(state, payload) {
    state.items = payload
  },
  addLabel(state, label) {
    state.items.unshift(label)
  },
  deleteLabel(state, labelId) {
    state.items = state.items.filter(item => item.id !== labelId)
  },
  updateSelected(state, selected) {
    state.selected = selected
  },
  updateLabel(state, label) {
    const item = state.items.find(item => item.id === label.id)
    Object.assign(item, label)
  },
  resetSelected(state) {
    state.selected = []
  },
  setLoading(state, payload) {
    state.loading = payload
  }
}

export const actions = {
  getLabelList({ commit }, payload) {
    commit('setLoading', true)
    return LabelService.getLabelList(payload.projectId)
      .then((response) => {
        commit('setLabelList', response.data)
      })
      .catch((error) => {
        alert(error)
      })
      .finally(() => {
        commit('setLoading', false)
      })
  },
  createLabel({ commit }, data) {
    return LabelService.addLabel(data.projectId, data)
      .then((response) => {
        commit('addLabel', response.data)
      })
  },
  updateLabel({ commit }, data) {
    LabelService.updateLabel(data.projectId, data.id, data)
      .then((response) => {
        commit('updateLabel', response.data)
      })
      .catch((error) => {
        alert(error)
      })
  },
  deleteLabel({ commit, state }, projectId) {
    for (const label of state.selected) {
      LabelService.deleteLabel(projectId, label.id)
        .then((response) => {
          commit('deleteLabel', label.id)
        })
        .catch((error) => {
          alert(error)
        })
    }
    commit('resetSelected')
  }
}
