export const state = () => ({
  username: null,
  isAuthenticated: false
})

export const mutations = {
  setUsername(state, username) {
    state.username = username
  },
  clearUsername(state) {
    state.username = null
  },
  setAuthenticated(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated
  }
}

export const getters = {
  isAuthenticated(state) {
    return state.isAuthenticated
  },
  getUsername(state) {
    return state.username
  }
}

export const actions = {
  authenticateUser({ commit }, authData) {
    this.$services.auth.login(authData.username, authData.password)
    commit('setAuthenticated', true)
  },
  async initAuth({ commit }) {
    try {
      const user = await this.$services.user.getMyProfile()
      commit('setAuthenticated', true)
      commit('setUsername', user.username)
    } catch {
      commit('setAuthenticated', false)
    }
  },
  logout({ commit }) {
    this.$services.auth.logout()
    commit('setAuthenticated', false)
    commit('clearUsername')
  }
}
