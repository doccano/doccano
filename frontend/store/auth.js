import Cookie from 'js-cookie'
import ApiService from '@/services/api.service'
import AuthService from '@/services/auth.service'

export const state = () => ({
  token: null,
  username: null
})

export const mutations = {
  setToken(state, token) {
    state.token = token
  },
  clearToken(state) {
    state.token = null
  },
  setUsername(state, username) {
    state.username = username
  },
  clearUsername(state) {
    state.username = null
  }
}

export const getters = {
  isAuthenticated(state) {
    return state.token != null
  },
  getUsername: () => () => {
    return localStorage.getItem('username')
  }
}

export const actions = {
  authenticateUser({ commit }, authData) {
    return AuthService.postCredential(authData)
      .then((result) => {
        commit('setToken', result.data.token)
        commit('setUsername', authData.username)
        localStorage.setItem('token', result.data.token)
        localStorage.setItem('username', authData.username)
        Cookie.set('jwt', result.data.token)
        ApiService.setHeader(result.data.token)
      })
  },
  initAuth({ commit, dispatch }, req) {
    let token
    if (req) {
      if (!req.headers.cookie) {
        return
      }
      const jwtCookie = req.headers.cookie
        .split(';')
        .find(c => c.trim().startsWith('jwt='))
      if (!jwtCookie) {
        return
      }
      token = jwtCookie.split('=')[1]
    } else {
      token = localStorage.getItem('token')
    }
    commit('setToken', token)
    ApiService.setHeader(token)
  },
  logout({ commit }) {
    commit('clearToken')
    commit('clearUsername')
    Cookie.remove('jwt')
    if (process.client) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    }
  }
}
