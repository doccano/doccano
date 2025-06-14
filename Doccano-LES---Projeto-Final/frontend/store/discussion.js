export const state = () => ({
  discussionsByProject: {} // Armazena estado por project_id: { projectId: { isDiscussionEnded: boolean } }
})

export const mutations = {
  setDiscussionEnded(state, { projectId, isEnded }) {
    // Criar um novo objeto para garantir reatividade
    const newState = { ...state.discussionsByProject }
    newState[projectId] = { isDiscussionEnded: isEnded }
    state.discussionsByProject = newState
  }
}

export const getters = {
  isDiscussionEnded: (state) => (projectId) => {
    return state.discussionsByProject[projectId]?.isDiscussionEnded || false
  }
}

export const actions = {
  endDiscussion({ commit }, projectId) {
    commit('setDiscussionEnded', { projectId, isEnded: true })
    // Persistir isso em localStorage para manter o estado entre recarregamentos
    if (process.client) {
      const discussionsState = JSON.parse(localStorage.getItem('discussionsState') || '{}')
      discussionsState[projectId] = { isDiscussionEnded: true }
      localStorage.setItem('discussionsState', JSON.stringify(discussionsState))
    }
  },
  
  reopenDiscussion({ commit }, projectId) {
    commit('setDiscussionEnded', { projectId, isEnded: false })
    // Atualizar localStorage
    if (process.client) {
      const discussionsState = JSON.parse(localStorage.getItem('discussionsState') || '{}')
      if (discussionsState[projectId]) {
        discussionsState[projectId].isDiscussionEnded = false
      }
      localStorage.setItem('discussionsState', JSON.stringify(discussionsState))
    }
  },
  
  initDiscussionState({ commit }) {
    if (process.client) {
      const discussionsState = JSON.parse(localStorage.getItem('discussionsState') || '{}')
      Object.keys(discussionsState).forEach(projectId => {
        const projectState = discussionsState[projectId]
        commit('setDiscussionEnded', { 
          projectId, 
          isEnded: projectState.isDiscussionEnded || false 
        })
      })
    }
  }
} 