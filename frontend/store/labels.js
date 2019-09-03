import LabelService from '@/services/label.service'

export const state = () => ({
  items: [],
  selected: []
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
  }
}

export const actions = {
  getLabelList(context, config) {
    return LabelService.getLabelList()
      .then((response) => {
        context.commit('setLabelList', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  addMember({ commit }, data) {
    LabelService.addLabel(data.projectId, data.labelId, data)
      .then((response) => {
        commit('addLabel', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  updateLabel({ commit }, data) {
    LabelService.updateLabel(data.projectId, data.labelId, data)
      .then((response) => {
        commit('updateLabel', response)
      })
      .catch((error) => {
        alert(error)
      })
  },
  removeLabel({ commit, state }, projectId) {
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
