export const state = () => ({
  username: null,
  id: null,
  isAuthenticated: false,
  isStaff: false,
  role: null
})

export const mutations = {
  setUsername(state, username) {
    state.username = username
  },
  setUserId(state, userId) {
    state.id = userId
  },
  clearUsername(state) {
    state.username = null
  },
  setAuthenticated(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated
  },
  setIsStaff(state, isStaff) {
    state.isStaff = isStaff
  },
  setRole(state, role) {
    state.role = role
  },
  updateUser(state, user) {
    state.username = user.username
    state.id = user.id
    state.isStaff = user.is_staff
    state.role = user.is_staff ? 'admin' : 'annotator'
  }
}

export const getters = {
  isAuthenticated(state) {
    return state.isAuthenticated
  },
  getUsername(state) {
    return state.username
  },
  getUserId(state) {
    return state.id
  },
  isStaff(state) {
    return state.isStaff
  },
  getRole(state) {
    return state.role
  }
}

export const actions = {
  async authenticateUser({ commit }, authData) {
    try {
      await this.$repositories.auth.login(authData.username, authData.password)
      commit('setAuthenticated', true)
    } catch (error) {
      throw new Error('The credential is invalid')
    }
  },
  async fetchSocialLink() {
    return await this.$repositories.auth.socialLink()
  },
  async initAuth({ commit }) {
    try {
      const user = await this.$repositories.user.getProfile()
      commit('setAuthenticated', true)
      commit('setUsername', user.username)
      commit('setUserId', user.id)
      commit('setIsStaff', user.isStaff)
      commit('setRole', user.isStaff ? 'admin' : 'annotator')
    } catch {
      commit('setAuthenticated', false)
      commit('setIsStaff', false)
      commit('setRole', 'annotator')
    }
  },
  async logout({ commit }) {
    await this.$repositories.auth.logout()
    commit('setAuthenticated', false)
    commit('setIsStaff', false)
    commit('clearUsername')
    commit('setRole', 'annotator')
  },
  async registerUser(_, userData) {
    try {
      return await this.$repositories.user.register(userData)
    } catch (error) {
      throw new Error('User registration failed')
    }
  }
}