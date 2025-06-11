export const state = () => ({
  list: []
})

export const getters = {
  list(state) {
    return state.list
  }
}

export const mutations = {
  setList(state, labels) {
    state.list = labels
  },
  addLabel(state, label) {
    state.list.push(label)
  },
  updateLabel(state, updatedLabel) {
    const index = state.list.findIndex(label => label.id === updatedLabel.id)
    if (index !== -1) {
      state.list.splice(index, 1, updatedLabel)
    }
  },
  removeLabel(state, labelId) {
    state.list = state.list.filter(label => label.id !== labelId)
  }
}

export const actions = {
  async fetch({ commit }, projectId) {
    try {
      // Determinar o tipo de label baseado no tipo de projeto
      // Por padrão, usamos categoryType, mas isso pode ser ajustado
      const labels = await this.$repositories.categoryType.list(projectId)
      commit('setList', labels)
      return labels
    } catch (error) {
      console.error('Erro ao buscar labels:', error)
      commit('setList', [])
      return []
    }
  },

  async create({ commit }, { projectId, label }) {
    try {
      const newLabel = await this.$repositories.categoryType.create(projectId, label)
      commit('addLabel', newLabel)
      return newLabel
    } catch (error) {
      console.error('Erro ao criar label:', error)
      throw error
    }
  },

  async update({ commit }, { projectId, label }) {
    try {
      const updatedLabel = await this.$repositories.categoryType.update(projectId, label)
      commit('updateLabel', updatedLabel)
      return updatedLabel
    } catch (error) {
      console.error('Erro ao atualizar label:', error)
      throw error
    }
  },

  async delete({ commit }, { projectId, labelId }) {
    try {
      await this.$repositories.categoryType.bulkDelete(projectId, [labelId])
      commit('removeLabel', labelId)
    } catch (error) {
      console.error('Erro ao deletar label:', error)
      throw error
    }
  }
}
